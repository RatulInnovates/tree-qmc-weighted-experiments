# MSA validation report (Phase 3)

Source: `weighted_qmc_msa_demo (1).zip`, extracted to `outputs/msa_input/` (originals untouched; zip kept). Format: FASTA, DNA. README says these are tiny synthetic teaching files, not research data.

| File | Taxa | Length | Equal length | Unique names | Gap chars | Ambiguous (non-ACGT,-) | Verdict |
|---|---|---|---|---|---|---|---|
| clean_gene1.fasta | 6 | [24] | True | True | 0 | 0 | OK |
| clean_gene2.fasta | 6 | [24] | True | True | 0 | 0 | OK |
| poor_gene1_demo.fasta | 6 | [24, 25, 26] | False | True | 10 | 0 | NOT OK: unequal lengths |
| poor_gene2_demo.fasta | 6 | [24, 25] | False | True | 10 | 0 | NOT OK: unequal lengths |

## Interpretation
- `clean_gene1/2.fasta`: valid, 6 taxa (A-F) x 24 sites, no gaps. Usable.
- `poor_gene1/2_demo.fasta`: sequences have different lengths (gap insertions/deletions were added without keeping columns aligned), so they are **not valid alignments**; IQ-TREE would reject them. I did not modify them; a fixed copy would require inventing alignment decisions, so I'm leaving them out unless you want a padded copy.
- Only 24 sites per gene: far too short for a reliable gene tree. Fine for a pipeline test only.
