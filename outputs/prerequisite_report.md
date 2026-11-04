# Prerequisite report (Phase 2)

Terminal: Claude Code ran in Git Bash / PowerShell 5.1. Builds and TREE-QMC runs use the MSYS2 **UCRT64** environment (`C:\msys64`, `/ucrt64/bin` on PATH).

## Initial state (before any install)
g++, make, CMake, IQ-TREE 3 and the demo MSA were all missing/not found; Git and Python were present. The paths in the original prompt (`C:\msys64`, `C:\Users\HP\...`) did not exist on this PC (user is `USER`).

## Current state (after installs you approved)
| Dependency | Installed? | Version | Status | Required Action |
|---|---|---|---|---|
| g++ | Yes (MSYS2 UCRT64) | g++.exe (Rev6, Built by MSYS2 project) 16.2.0 | OK | Only visible in UCRT64 shell / with `C:\msys64\ucrt64\bin` on PATH |
| GNU Make | Yes (MSYS2) | GNU Make 4.4.1 | OK | same |
| CMake | No | - | Not needed (README g++ build used) | Only needed for the official CMake route, which also needs R+RInside+Rcpp+MSCquartets |
| Git | Yes | git version 2.55.0.windows.3 | OK | none |
| Python 3 | Yes | Python 3.14.7 | OK (used for helper scripts only) | none |
| IQ-TREE 3 | Yes (downloaded) | 3.1.4 | OK | `outputs/tools/iqtree/iqtree-3.1.4-Windows/bin/iqtree3.exe` |
| Extra libraries | Bundled | MQLib, toms743 | OK | none |
| Demo MSA | Yes | 4 FASTA files | 2 valid, 2 invalid | see msa_validation_report.md |
