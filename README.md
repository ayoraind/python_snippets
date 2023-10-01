## Python code snippets for quick microbial genomics analysis (bioinformatics).
### Usage


## Introduction
This repository contains three (and counting) python snippets for parsing genome annotation outputs.  
1. The extract_protein_sequence_from_gbff.py scripts scans GBFF files for a named gene and extract protein sequences. The `-parent_directory` is the path to the parent directory containing subdirectories with GBFF files. The `--gene_name` is the exact name of the gene to search for (it must be a valid gene name). The `--output_directory` is the file path to the output directory

### Sample command
An example of a command to run this code snippet is:

```
extract_protein_sequence_from_gbff.py --parent_directory "Sample_files" --gene_name "blaNDM-1" --output_directory "test_out"
```
