import json, statistics as st, collections
R = json.load(open("results.json"))
by = collections.defaultdict(dict)
for x in R: by[(x["cond"], x["rep"])][x["method"]] = x
lines = ["# Weighted vs unweighted TREE-QMC: simulation results\n",
 "Species-tree error = normalised unrooted Robinson-Foulds distance to the true species tree (0 = perfect, 1 = nothing shared). Lower is better.\n",
 "| Condition | Mean gene-tree error (RF) | Unweighted TREE-QMC | Weighted (--hybrid --bootstrap) | Replicates: weighted better / tie / worse |",
 "|---|---|---|---|---|"]
for cond in ["true_gene_trees", "L100", "L400"]:
    reps = [v for (c, r), v in sorted(by.items()) if c == cond]
    if not reps: continue
    u = [v["unweighted"]["rf"] for v in reps]
    g = st.mean(v["unweighted"]["gtee"] for v in reps)
    if "hybrid" in reps[0]:
        h = [v["hybrid"]["rf"] for v in reps]
        wl = sum(a < b for a, b in zip(h, u)); t = sum(a == b for a, b in zip(h, u)); lo = sum(a > b for a, b in zip(h, u))
        lines.append(f"| {cond} | {g:.3f} | {st.mean(u):.3f} (sd {st.pstdev(u):.3f}) | {st.mean(h):.3f} (sd {st.pstdev(h):.3f}) | {wl} / {t} / {lo} |")
    else:
        lines.append(f"| {cond} (control, no estimation error) | 0 | {st.mean(u):.3f} (sd {st.pstdev(u):.3f}) | n/a | n/a |")
lines.append("\nPer-replicate values are in `results.tsv`.")
open("results_table.md", "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
