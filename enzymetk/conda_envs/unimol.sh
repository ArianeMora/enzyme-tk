#!/bin/bash

conda create -n unimol --channel conda-forge python=3.11 -y
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh

conda activate unimol
pip install unimol_tools
pip install huggingface_hub
