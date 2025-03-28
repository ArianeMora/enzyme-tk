#!/bin/bash
# Install FastTree
conda install -c bioconda -c conda-forge diamond -y
conda update diamond

# downloading and using a BLAST database
# update_blastdb.pl --decompress --blastdb_version 5 swissprot
# ./diamond prepdb -d swissprot
