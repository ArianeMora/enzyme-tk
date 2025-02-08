#!/bin/bash
# Foldseek
# Doesn't like working with conda init
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda activate enzymetk
conda install -c conda-forge -c bioconda foldseek -y
conda install -c conda-forge -c bioconda mmseqs2 -y