export PATH=/ucrt64/bin:/usr/bin:$PATH
cd "/d/_Personal/Random Projects/TREE-QMC/outputs"
T=tqmc_pre_network/build/tree-qmc.exe
$T -h > treeqmc_help.txt
echo "### Test A: 2 clean gene trees (pipeline check only)"
$T -i gene_trees/gene_trees.tre -o species_tree/species_tree.nwk --override; echo "exit=$?"; cat species_tree/species_tree.nwk
echo "### Test B: bundled avian dataset, 3679 gene trees (program-level test)"
time $T -i iq_work/avian_clean.tre -a ../tutorial/gene-trees/avian_name_map.txt -o species_tree/avian_species_tree.nwk --override; echo "exit=$?"
head -c 250 species_tree/avian_species_tree.nwk; echo
