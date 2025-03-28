#!/bin/bash
# Proteinfer
conda create --name proteinfer -c conda-forge python=3.7.12 -y
# Doesn't like working with conda init
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda activate proteinfer
pip3 install -r proteinfer_requirements.txt

git clone https://github.com/google-research/proteinfer
cd proteinfer
python3 install_models.py
