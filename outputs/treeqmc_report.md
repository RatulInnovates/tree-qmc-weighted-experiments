# TREE-QMC report (Phase 6)
Input: Newick gene trees, one per line. Command: `tree-qmc.exe -i <gene trees> -o <species tree> --override` (`-i` input, `-o` output, `--override` overwrite). Run via `run_tqmc.sh` / `run_avian.sh`. Logs: `treeqmc_log.txt`.

| Test | Input | Output | Status |
|---|---|---|---|
| A. pipeline check | your 2 clean gene trees (6 taxa) | `species_tree/species_tree.nwk` = `(((C,F),B),((A,D),E));` | runs, valid Newick, 6 leaves. **NOT scientifically meaningful**: 2 genes of 24 sites |
| B1. program-level | tutorial avian set, 3679 real gene trees, unweighted | `species_tree/avian_unweighted.nwk` | valid Newick, 48 leaves, ~35 s |
| B2. weighted | same, `--hybrid --bootstrap --root STRCA,TINMA` (Weighted TREE-QMC, from tutorial) | `species_tree/avian_hybrid.nwk` | valid Newick, 48 leaves, ~35 s |

No fake or duplicated gene trees were used. Validity check = trailing `;`, balanced parentheses, expected leaf count (not a topology comparison). The avian trees were not compared to a reference; I did not claim accuracy.
Note: the tutorial's `avian_name_map.txt` is a label file, not an `-a` mapping file, so it was not used.
