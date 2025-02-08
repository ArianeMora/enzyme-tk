#!/bin/bash
# Docko
conda  create --name docko python=3.10.14 -y
conda activate docko
conda install -c conda-forge pdbfixer -y
conda config --env --add channels conda-forge
pip install git+https://github.com/chaidiscovery/chai-lab.git