# FINAL TEST REPORT
1. **Repository:** TREE-QMC 4.1.5 (C++), implements TREE-QMC + Weighted TREE-QMC (+ TOB-QMC, NetCS). Takes Newick gene trees. See `project_inspection.md`.
2. **Prerequisites:** initially missing g++, make, CMake, IQ-TREE; Git/Python OK. Installed with permission: MSYS2 (gcc 16.2, make 4.4.1) and IQ-TREE 3.1.4. CMake and R not installed (not needed). `prerequisite_report.md` now shows the current state.
3. **MSA:** clean_gene1/2 valid (6 taxa x 24 sites); poor_gene1/2 invalid (unequal lengths, left unmodified, not used). `msa_validation_report.md`.
4. **Compile:** SUCCESS, but not on current `main` (upstream non-TOB build bug); built older commit 7f840e7 in a worktree. `build_report.md`.
5. **IQ-TREE:** SUCCESS for both clean genes. `iqtree_report.md`.
6. **TREE-QMC:** SUCCESS on all runs (2-gene pipeline test; avian 3679-gene unweighted and weighted). `treeqmc_report.md`.
7. **Simulation study (weighted vs unweighted):** see `simulation/SIMULATION_REPORT.md`. 5 replicates x 100 genes x 2 error levels, plus few-gene subsets: weighted (`--hybrid --bootstrap`) was equal or slightly better in every setting (e.g. 5 genes/100 bp: RF 0.223 vs 0.240), never worse on average; effect small, 5 species trees only, subsets not independent.
7b. **Outputs:** gene_trees/{gene1,gene2}.treefile, gene_trees.tre; species_tree/{species_tree,avian_unweighted,avian_hybrid}.nwk; logs and reports in this folder.
8. **Errors & fixes:** M_PI (flag), Network type (older commit), segfault (wrong shell/DLL PATH), wrong mapping file (not needed).
9. **Limitations:** 2 genes x 24 sites is a plumbing test only; main-branch build unresolved; poor-alignment examples unusable as-is; no accuracy evaluation done; weighted mode was only exercised on avian data, not on your IQ-TREE trees (no support values).
10. **Next steps:** (a)-(c) DONE in `simulation/`; remaining: more replicates/taxa, alignment/homology errors, missing data, statistical test; (d) decide whether to patch `instance.hpp` or install R for the main-branch build.
