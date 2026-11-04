# IQ-TREE report (Phase 5)
- IQ-TREE 3.1.4 downloaded from github.com/iqtree/iqtree3 releases (`outputs/tools/`). Works.
- Command (per gene): `iqtree3.exe -s msa_input/clean_geneN.fasta -m MFP --seed 12345 -T 1 --prefix iq_work/geneN`
  - `-s` alignment, `-m MFP` automatic model selection, `--seed` reproducibility, `-T 1` one thread.
- Only the two valid alignments (clean_gene1, clean_gene2) were used; the "poor" ones have unequal lengths (see MSA report).
- Results: gene1 model TN+I, gene2 model K2P+I. Trees: `gene_trees/gene1.treefile`, `gene2.treefile`; combined one-per-line file `gene_trees/gene_trees.tre`. Full IQ-TREE reports in `iqtree_full/`, log in `iqtree_log.txt`.
- A treefile is an unrooted Newick tree (parentheses = clades, numbers = branch lengths in substitutions/site). **Caution:** 24 sites is tiny; many branches have ~0 length (e.g. gene1 is nearly a polytomy), so these trees are barely informative.
