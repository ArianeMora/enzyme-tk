#!/bin/bash
# The base enzymetk env which works with most tools
conda create --name enzymetk python==3.11.8 -y
# Doesn't like working with conda init
# Doesn't like working with conda init
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh

conda activate enzymetk
pip install -r base_requirements.txt
conda install pytorch::faiss-gpu -y
conda install -c conda-forge pyarrow -y
pip install transformers
