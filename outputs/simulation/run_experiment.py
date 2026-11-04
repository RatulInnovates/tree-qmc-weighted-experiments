"""Weighted vs unweighted TREE-QMC on simulated data.
Pipeline per replicate: random species tree -> MSC gene trees -> AliSim alignments
(two lengths = two error levels) -> IQ-TREE ML trees + UFBoot -> TREE-QMC (unweighted / hybrid)
-> compare with the true species tree (unrooted RF). Resumable: finished files are skipped.
Usage: python -I run_experiment.py
"""
import os, random, subprocess, re, json, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
IQ = os.path.join(OUT, "tools/iqtree/iqtree-3.1.4-Windows/bin/iqtree3.exe")
TQMC = os.path.join(OUT, "tqmc_pre_network/build/tree-qmc.exe")
WORK = os.path.join(HERE, "work")
NTAX, NGENES, REPS, LENGTHS, MU = 16, 100, [1, 2, 3, 4, 5], [100, 400], 0.05
if os.environ.get("SMOKE"):  # quick self-test
    NGENES, REPS, LENGTHS = 10, [1], [200]
    WORK = os.path.join(HERE, "work_smoke")
MODEL = "GTR{1,2,1,1,2}+F{0.3,0.2,0.2,0.3}+G4{0.5}"   # true model, used for simulation
ENV = dict(os.environ, PATH=r"C:\msys64\ucrt64\bin;" + os.environ["PATH"])  # runtime DLLs for tree-qmc
NW = 10


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, env=ENV, **kw)


# ---------- minimal Newick utilities ----------
def parse(s):
    """Return nested lists; leaves are str. Branch lengths/support labels are dropped."""
    s = s.strip().rstrip(";")
    pos = 0
    def node():
        nonlocal pos
        if s[pos] == "(":
            pos += 1
            kids = [node()]
            while s[pos] == ",":
                pos += 1
                kids.append(node())
            pos += 1  # ')'
            while pos < len(s) and s[pos] not in ",)":
                pos += 1  # skip label / :length
            return kids
        m = re.match(r"[^,():;]+", s[pos:])
        pos += m.end()
        name = m.group(0).strip()
        while pos < len(s) and s[pos] not in ",)":
            pos += 1
        return name
    return node()


def leaves(t):
    return [t] if isinstance(t, str) else [x for c in t for x in leaves(c)]


def bipartitions(t):
    """Nontrivial unrooted splits, each as the frozenset NOT containing the smallest taxon."""
    allt = frozenset(leaves(t)); ref = min(allt); out = set()
    def rec(n):
        if isinstance(n, str):
            return frozenset([n])
        sset = frozenset().union(*[rec(c) for c in n])
        if 1 < len(sset) < len(allt) - 1:
            out.add(sset if ref not in sset else allt - sset)
        return sset
    rec(t)
    return out


def rf(a, b):
    """Normalised unrooted Robinson-Foulds (0 = identical, 1 = no shared splits)."""
    A, B = bipartitions(parse(a)), bipartitions(parse(b))
    d = len(A ^ B); m = len(A) + len(B)
    return d / m if m else 0.0


# ---------- simulation ----------
def species_tree(rng):
    lin = [(f"T{i+1:02d}", 0.0) for i in range(NTAX)]
    h = 0.0; nodes = {}
    def mk(n): return n
    items = [dict(name=n, h=0.0, kids=None) for n, _ in lin]
    while len(items) > 1:
        h += rng.uniform(0.1, 0.5)                      # internal branch 0.1-0.5 coalescent units (high ILS)
        a, b = rng.sample(items, 2)
        items = [x for x in items if x is not a and x is not b] + [dict(name=None, h=h, kids=[a, b])]
    return items[0]


def sp_newick(n):
    return n["name"] if n["kids"] is None else "(" + ",".join(sp_newick(k) for k in n["kids"]) + ")"


def msc_gene_tree(sp, rng):
    def sim(n, upper):
        if n["kids"] is None:
            lins = [(n["name"], 0.0)]
        else:
            lins = [l for k in n["kids"] for l in sim(k, n["h"])]
        t = n["h"]
        while len(lins) > 1:
            k = len(lins)
            t += rng.expovariate(k * (k - 1) / 2)
            if t > upper:
                break
            (s1, h1), (s2, h2) = rng.sample(lins, 2)
            lins = [x for x in lins if x[0] is not s1 and x[0] is not s2] + \
                   [(f"({s1}:{(t-h1)*MU:.8f},{s2}:{(t-h2)*MU:.8f})", t)]
        return lins
    (s, _), = sim(sp, float("inf"))
    return s + ";"


def alisim_and_iq(args):
    d, g, L, gt = args
    base = os.path.join(d, f"g{g:03d}")
    est = base + ".est.treefile"
    if os.path.exists(est):
        return
    open(base + ".true.tre", "w").write(gt + "\n")
    if not os.path.exists(base + ".fa"):
        run([IQ, "--alisim", base, "-m", MODEL, "-t", base + ".true.tre", "--length", str(L),
             "--seed", str(g + 1000 * L), "-af", "fasta"])
    fa = base + ".fa"
    run([IQ, "-s", fa, "-m", "GTR+G4", "-B", "1000", "--seed", "1", "-T", "1", "-quiet",
         "--prefix", base + ".est"])


def tqmc(inp, out, extra):
    if not os.path.exists(out):
        run([TQMC, "-i", inp, "-o", out, "--override"] + extra)


def main():
    os.makedirs(WORK, exist_ok=True)
    results = []
    for r in REPS:
        rng = random.Random(r)
        sp = species_tree(rng)
        true_sp = sp_newick(sp) + ";"
        rdir = os.path.join(WORK, f"rep{r}"); os.makedirs(rdir, exist_ok=True)
        open(os.path.join(rdir, "true_species.nwk"), "w").write(true_sp + "\n")
        gts_file = os.path.join(rdir, "true_gene_trees.json")
        if os.path.exists(gts_file):
            gts = json.load(open(gts_file))
        else:
            gts = [msc_gene_tree(sp, rng) for _ in range(NGENES)]
            json.dump(gts, open(gts_file, "w"))
        # control: TREE-QMC on the true (error-free) gene trees
        open(os.path.join(rdir, "true_gene_trees.tre"), "w").write("\n".join(gts) + "\n")
        tqmc(os.path.join(rdir, "true_gene_trees.tre"), os.path.join(rdir, "sp_truegt.nwk"), [])
        results.append(dict(rep=r, cond="true_gene_trees", method="unweighted", L=0, gtee=0.0,
                            rf=rf(open(os.path.join(rdir, "sp_truegt.nwk")).read(), true_sp)))
        for L in LENGTHS:
            d = os.path.join(rdir, f"L{L}"); os.makedirs(d, exist_ok=True)
            print(f"rep{r} L{L}: simulating + estimating {NGENES} genes", flush=True)
            with ThreadPoolExecutor(NW) as ex:
                list(ex.map(alisim_and_iq, [(d, g, L, gts[g]) for g in range(NGENES)]))
            est = []; gtee = []
            for g in range(NGENES):
                f = os.path.join(d, f"g{g:03d}.est.treefile")
                if os.path.exists(f):
                    t = open(f).read().strip(); est.append(t)
                    gtee.append(rf(t, gts[g]))
            open(os.path.join(d, "est_gene_trees.tre"), "w").write("\n".join(est) + "\n")
            mean_g = sum(gtee) / len(gtee)
            print(f"  estimated {len(est)} gene trees, mean gene-tree RF error {mean_g:.3f}", flush=True)
            for name, extra in [("unweighted", []),
                                ("hybrid", ["--hybrid", "--bootstrap"])]:
                out = os.path.join(d, f"sp_{name}.nwk")
                tqmc(os.path.join(d, "est_gene_trees.tre"), out, extra)
                results.append(dict(rep=r, cond=f"L{L}", method=name, L=L, gtee=mean_g,
                                    rf=rf(open(out).read(), true_sp)))
                print(f"  {name}: species-tree RF = {results[-1]['rf']:.3f}", flush=True)
    json.dump(results, open(os.path.join(HERE, "results.json"), "w"), indent=1)
    with open(os.path.join(HERE, "results.tsv"), "w") as f:
        f.write("replicate\tcondition\tmethod\tseq_length\tmean_gene_tree_RF_error\tspecies_tree_RF\n")
        for x in results:
            f.write(f"{x['rep']}\t{x['cond']}\t{x['method']}\t{x['L']}\t{x['gtee']:.4f}\t{x['rf']:.4f}\n")
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
