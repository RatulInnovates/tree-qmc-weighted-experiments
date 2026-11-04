# Build report (Phase 4)
- Toolchain (installed with your permission): MSYS2 via winget -> `pacman -S mingw-w64-ucrt-x86_64-gcc make`. Built from the UCRT64 environment.
- **Issue 1 (MQLib):** `'M_PI' was not declared` (MinGW + `-std=c++0x`). Fix with no source edit: `make CFLAGS="... -D_USE_MATH_DEFINES"`.
- **Issue 2 (TREE-QMC at current `main`):** the README's non-TOB build fails (`'Network' does not name a type`): `src/instance.hpp` uses `Network` but only includes `network.hpp` when `ENABLE_TOB` is set (upstream bug). The official CMake route needs R + RInside + Rcpp + MSCquartets (not installed).
- **Workaround (no edits to your files):** built the upstream commit `7f840e7` ("Updated to enable build without TOB functionality", still version 4.1.5, still has weighted options) in a separate git worktree `outputs/tqmc_pre_network/` using the README command. Your `src/` is untouched.
- Result: `outputs/tqmc_pre_network/build/tree-qmc.exe` (655 KB). `-h` works; full help saved in `treeqmc_help.txt`. Log: `build_log.txt`; script: `build.sh`.
- Gotcha: run it from the MSYS2 UCRT64 shell (or with `/ucrt64/bin` on PATH). From plain Git Bash it crashed with a segfault (missing runtime DLLs).
