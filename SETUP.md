# Reproduce on another Windows PC
1. Install MSYS2: `winget install --id MSYS2.MSYS2 -e`; in an MSYS2 **UCRT64** shell: `pacman -S mingw-w64-ucrt-x86_64-gcc make`.
2. Download IQ-TREE 3.1.4 (Windows zip) from https://github.com/iqtree/iqtree3/releases and unzip to `outputs/tools/iqtree/iqtree-3.1.4-Windows/`.
3. Get TREE-QMC and build the **older commit** (current `main` fails without R; `instance.hpp` uses `Network` unguarded):
   ```
   git clone https://github.com/molloy-lab/TREE-QMC outputs/tqmc_pre_network
   cd outputs/tqmc_pre_network && git checkout 7f840e7
   ```
   then run `outputs/build.sh` from the UCRT64 shell (it adds `-D_USE_MATH_DEFINES` for MQLib's `M_PI`; adjust the `cd` path inside).
4. Run `tree-qmc.exe` only with `C:\msys64\ucrt64\bin` on PATH (otherwise it segfaults).
5. Simulation: `cd outputs/simulation && python -I run_experiment.py && python -I analyze.py && python -I subsample.py` (~15 min, 10 threads). Needs Python 3 only (stdlib).
