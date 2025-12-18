#!/bin/bash
# CARE processing
conda create -n CARE_processing python=3.8 -y
# Doesn't like working with conda init
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda activate CARE_processing
conda install -c mamba-forge -c bioconda mmseqs2 -y
conda install -c rdkit rdkit=2020.03.3 -y
pip install -r care_requirements.txt

# CREEP environment
git clone git@github.com:jsunn-y/CARE.git
cd CARE/CREEP
conda create -n CREEP python=3.8
# Doesn't like working with conda init
mamba_BASE=$(conda info --base)
source $mamba_BASE/etc/profile.d/conda.sh
conda activate CREEP
#we recommend installing this way so that torch is compatible with your GPU and your version of CUDA
pip install pandas torch==2.2.0 transformers==4.39.1 sentencepiece
pip install -e .