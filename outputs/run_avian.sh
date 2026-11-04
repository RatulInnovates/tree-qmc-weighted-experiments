export PATH=/ucrt64/bin:/usr/bin:$PATH
cd "/d/_Personal/Random Projects/TREE-QMC/outputs"
T=tqmc_pre_network/build/tree-qmc.exe
echo "### Test B1: avian, unweighted"
time $T -i iq_work/avian_clean.tre -o species_tree/avian_unweighted.nwk --override; echo "exit=$?"
echo "### Test B2: avian, weighted (--hybrid --bootstrap --root STRCA,TINMA)"
time $T --hybrid --bootstrap --root STRCA,TINMA -i iq_work/avian_clean.tre -o species_tree/avian_hybrid.nwk --override; echo "exit=$?"
