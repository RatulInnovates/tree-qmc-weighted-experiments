# Project inspection (Phase 1)

- **Language:** C++ (C++11 per README build; CMakeLists.txt asks for C++20).
- **Entry point:** `main()` in `src/tqmc.cpp`. Version: 4.1.5 (`version.txt`).
- **Main sources:** `src/*.cpp` (tree.cpp, tree_w.cpp, tree_s.cpp, graph.cpp, species_tree.cpp, tree_of_blobs.cpp, network*.cpp, ...).
- **Bundled dependencies:** `external/MQLib` (max-cut heuristic; must be built with `make` into `MQLib.a`) and `external/toms743` (Lambert W). No external system libraries beyond libm.
- **Implements:** TREE-QMC AND Weighted TREE-QMC (`-w h|s|l`, `--hybrid`, `-B/-L/-S` support presets), plus TOB-QMC (tree of blobs) and NetCS.
- **Input:** gene trees in Newick, one per line (`-i`). NOT raw MSAs by default. Exception: `--chars`/`--bp` accept character matrices (fasta/phylip/nexus) directly, i.e. a different mode from "MSA -> gene tree -> species tree". Optional `-a` mapping file (individual -> species).
- **Output:** one species tree in Newick (`-o`, default stdout). `--override` to overwrite.
- **Included examples:** `tutorial/gene-trees/avian_uce_trees_3679.tre` (3679 gene trees) + `avian_name_map.txt`; `tutorial/characters/4345ratites.nex`; `tutorial/NetCS/gt.trees`; `tutorial/quartets/*`; `tutorial/tree-of-blobs/nomiinae`.

## Official build (README, Linux-style bash)
```
cd external/MQLib && make
cd ../../ && mkdir -p build && cd build
g++ -std=c++11 -O2 -I ../external/MQLib/include -I ../external/toms743 -o tree-qmc \
    ../src/*.cpp ../external/toms743/toms743.cpp ../external/MQLib/bin/MQLib.a -lm -DVERSION=\"$(cat ../version.txt)\"
```
Alternative: CMake (`CMakeLists.txt`, needs CMake >= 3.18). The README says to see `tutorial/tree-of-blobs/README.md` for full build instructions (not yet read; to be checked before Phase 4).

## Run
`build/tree-qmc -i genetrees.tre -o species.tre` (add `-a map.txt` if multiple individuals per species). Help: `tree-qmc -h`.
Tip from README: Windows `\r` characters can break input; clean with `tr -d '\r'`.
