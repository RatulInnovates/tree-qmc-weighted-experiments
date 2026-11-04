# Simulation study: weighted vs unweighted TREE-QMC

## Design (all code in this folder; reproduce with `python -I run_experiment.py`, then `analyze.py`, `subsample.py`)
1. **Species trees:** 5 random 16-taxon trees (seeds 1-5), internal branches 0.1-0.5 coalescent units (substantial incomplete lineage sorting).
2. **Gene trees:** 100 per species tree, simulated under the multispecies coalescent (own Python simulator, 1 individual/species). Branch lengths converted to substitutions/site with rate 0.05 per coalescent unit.
3. **Alignments:** IQ-TREE 3 **AliSim**, model GTR+F+G4 (fixed parameters), two lengths: **100 bp (high error)** and **400 bp (lower error)**.
4. **Gene-tree estimation:** `iqtree3 -m GTR+G4 -B 1000` (true model family, ultrafast bootstrap supports).
5. **Species trees:** TREE-QMC (v4.1.5) unweighted vs weighted `--hybrid --bootstrap`.
6. **Metric:** normalised unrooted Robinson-Foulds distance to the true species tree (0 best). Also reported: gene-tree estimation error (RF to true gene tree).
7. **Few-gene test:** random subsets (5/10/20/40 genes, 10 draws each) of the estimated gene trees, same two methods.

## Results
Full run, 100 genes (`results_table.md`, `results.tsv`):

| Condition | Mean gene-tree error | Unweighted | Weighted | Weighted better/tie/worse (5 reps) |
|---|---|---|---|---|
| true gene trees (control) | 0 | 0.000 | n/a | n/a |
| 100 bp | 0.373 | 0.031 | 0.015 | 1 / 4 / 0 |
| 400 bp | 0.152 | 0.015 | 0.000 | 1 / 4 / 0 |

Few genes (`subsample_table.md`, `subsample_results.tsv`; 50 paired runs per row):

| bp | genes | Unweighted | Weighted | better/tie/worse |
|---|---|---|---|---|
| 100 | 5 | 0.240 | 0.223 | 22/17/11 |
| 100 | 10 | 0.151 | 0.143 | 14/25/11 |
| 100 | 20 | 0.086 | 0.083 | 14/27/9 |
| 100 | 40 | 0.043 | 0.035 | 8/38/4 |
| 400 | 5 | 0.178 | 0.155 | 15/30/5 |
| 400 | 10 | 0.082 | 0.071 | 8/39/3 |
| 400 | 20 | 0.045 | 0.042 | 4/44/2 |
| 400 | 40 | 0.017 | 0.015 | 1/49/0 |

## Interpretation
- With noisy gene trees (37% of gene-tree splits wrong at 100 bp), TREE-QMC still recovers the species tree well with 100 genes; the control with perfect gene trees is exact.
- Weighted TREE-QMC was **never worse on average and was better or equal in every row**; the gain is small in absolute terms (about 0.005-0.02 RF) and largest when data are scarce (5 genes) or noisy. This is directionally consistent with the Weighted TREE-QMC paper (Han & Molloy 2025), but it is a small experiment.

## Limitations (important)
- Only 5 species trees, 16 taxa, 1 individual per species. Subsets within a replicate are drawn from the same 100 genes, so the 50 runs per row are **not independent**; the better/tie/worse counts overstate confidence. No significance test was done.
- Simulated error comes only from short sequences (the true model is used for estimation); no systematic homology/alignment error, no missing data.
- Weighting uses UFBoot support (0-100) with the `--bootstrap` preset; I did not test other presets (`-w s`, `-w l`, `--lrt`).
- TREE-QMC version is the older commit 7f840e7 (see build_report.md).
- Suggested next steps: more replicates/taxa (e.g. 50), varying ILS levels, add alignment errors, missing data, and a paired statistical test across independent replicates.
