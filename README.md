# TREE-QMC / Weighted TREE-QMC: setup, test and simulation (Windows 11)

Records a beginner-friendly baseline run of [TREE-QMC](https://github.com/molloy-lab/TREE-QMC) on Windows, and a small simulation comparing **weighted vs unweighted** TREE-QMC.

Pipeline: `MSA -> IQ-TREE (gene trees) -> TREE-QMC -> species tree`. TREE-QMC takes gene trees (Newick), not raw alignments.

## Start reading here
1. `outputs/TREE-QMC_Test_Report.docx` - everything in one Word file (same content as the `.md` reports).
2. `outputs/FINAL_TEST_REPORT.md` - summary of all phases and problems solved.
3. `outputs/simulation/SIMULATION_REPORT.md` - weighted vs unweighted results (headline: weighted equal or slightly better everywhere; small effect, 5 species trees only).
4. `outputs/commands_used.txt` - every command, in order.

## Layout
- `outputs/*_report.md`, `project_inspection.md` - phases 1-6 reports
- `outputs/msa_input/` - demo MSAs (2 valid, 2 invalid) + original zip
- `outputs/gene_trees/`, `outputs/species_tree/` - IQ-TREE gene trees; TREE-QMC species trees (incl. avian 3679-gene runs)
- `outputs/simulation/` - scripts (`run_experiment.py`, `analyze.py`, `subsample.py`), results (`results.tsv`, `subsample_results.tsv`), and key data under `data/` (true species trees, estimated gene trees, inferred species trees)
- `outputs/build.sh`, `run_tqmc.sh`, `run_avian.sh` - build/run scripts

## Not included (too big / rebuildable) - see SETUP.md to recreate
IQ-TREE binaries, the compiled TREE-QMC, and raw per-gene simulation files.

Note: absolute Windows paths in the reports/scripts (`D:\_Personal\...`, `C:\msys64`) are from the original machine.
