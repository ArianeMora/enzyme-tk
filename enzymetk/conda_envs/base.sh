#!/bin/bash
# The base enzymetk env which works with most tools
conda create --name enzymetk -y
# Doesn't like working with mamba init
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh

conda activate enzymetk

# Do this at the end so it forces certain versions like pandas
uv pip install -r base_requirements.txt