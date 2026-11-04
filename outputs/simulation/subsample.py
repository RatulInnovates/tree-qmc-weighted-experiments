"""Harder test: few genes. Random subsets of the already-estimated gene trees -> TREE-QMC (unweighted vs hybrid)."""
import os, random, json, importlib.util as u, collections, statistics as st
sp = u.spec_from_file_location("e", "run_experiment.py"); e = u.module_from_spec(sp); sp.loader.exec_module(e)
rows = []
for r in e.REPS:
    rd = os.path.join(e.WORK, f"rep{r}"); true_sp = open(os.path.join(rd, "true_species.nwk")).read()
    for L in e.LENGTHS:
        trees = open(os.path.join(rd, f"L{L}", "est_gene_trees.tre")).read().split("\n"); trees = [t for t in trees if t]
        for k in (5, 10, 20, 40):
            for draw in range(10):
                rng = random.Random(1000 * r + 10 * k + draw)
                d = os.path.join(rd, f"L{L}", f"sub{k}_{draw}"); os.makedirs(d, exist_ok=True)
                f = os.path.join(d, "gt.tre"); open(f, "w").write("\n".join(rng.sample(trees, k)) + "\n")
                for name, extra in [("unweighted", []), ("hybrid", ["--hybrid", "--bootstrap"])]:
                    out = os.path.join(d, f"sp_{name}.nwk"); e.tqmc(f, out, extra)
                    rows.append(dict(rep=r, L=L, k=k, draw=draw, method=name, rf=e.rf(open(out).read(), true_sp)))
json.dump(rows, open("subsample_results.json", "w"))
with open("subsample_results.tsv", "w") as fh:
    fh.write("replicate\tseq_length\tn_genes\tdraw\tmethod\tspecies_tree_RF\n")
    for x in rows: fh.write(f"{x['rep']}\t{x['L']}\t{x['k']}\t{x['draw']}\t{x['method']}\t{x['rf']:.4f}\n")
g = collections.defaultdict(list)
for x in rows: g[(x["L"], x["k"], x["method"])].append(x["rf"])
pair = collections.defaultdict(lambda: [0, 0, 0])
by = {(x["rep"], x["L"], x["k"], x["draw"], x["method"]): x["rf"] for x in rows}
for (r, L, k, d, m), v in by.items():
    if m == "unweighted":
        h = by[(r, L, k, d, "hybrid")]; p = pair[(L, k)]; p[0 if h < v else 1 if h == v else 2] += 1
out = ["# Few-gene test (random subsets of estimated gene trees)\n",
       f"{len(e.REPS)} replicate species trees x 10 random subsets per cell = {len(e.REPS)*10} runs per cell. Mean species-tree RF (lower is better).\n",
       "| Seq length | # genes | Unweighted | Weighted (hybrid) | Weighted better / tie / worse |", "|---|---|---|---|---|"]
for L in e.LENGTHS:
    for k in (5, 10, 20, 40):
        a, b, p = g[(L, k, "unweighted")], g[(L, k, "hybrid")], pair[(L, k)]
        out.append(f"| {L} | {k} | {st.mean(a):.3f} | {st.mean(b):.3f} | {p[0]} / {p[1]} / {p[2]} |")
open("subsample_table.md", "w").write("\n".join(out) + "\n"); print("\n".join(out))
