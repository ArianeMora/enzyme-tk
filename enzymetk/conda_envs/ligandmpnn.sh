#!/bin/bash
conda create -n ligandmpnn_env python=3.11 -y
# Doesn't like working with conda init
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda activate ligandmpnn_env
pip3 install -r ligandmpnn_requirements.txt