# Weighted vs unweighted TREE-QMC: simulation results

Species-tree error = normalised unrooted Robinson-Foulds distance to the true species tree (0 = perfect, 1 = nothing shared). Lower is better.

| Condition | Mean gene-tree error (RF) | Unweighted TREE-QMC | Weighted (--hybrid --bootstrap) | Replicates: weighted better / tie / worse |
|---|---|---|---|---|
| true_gene_trees (control, no estimation error) | 0 | 0.000 (sd 0.000) | n/a | n/a |
| L100 | 0.373 | 0.031 (sd 0.038) | 0.015 (sd 0.031) | 1 / 4 / 0 |
| L400 | 0.152 | 0.015 (sd 0.031) | 0.000 (sd 0.000) | 1 / 4 / 0 |

Per-replicate values are in `results.tsv`.
