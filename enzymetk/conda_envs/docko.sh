#!/bin/bash
# Docko
conda  create --name docko python=3.10.14 -y
# Doesn't like working with conda init
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda activate docko
conda install -c conda-forge pdbfixer -y
conda config --env --add channels conda-forge
pip install git+https://github.com/chaidiscovery/chai-lab.git
pip install docko