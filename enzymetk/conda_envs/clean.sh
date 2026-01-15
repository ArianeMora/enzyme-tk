#!/bin/bash
# Clean
git clone https://github.com/tttianhao/CLEAN.git
# Also install porechop
conda create -n clean python==3.10.4 -y
# Doesn't like working with conda init
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda activate clean
pip install -r clean_requirements.txt
# If you have CPU you need to install the following:
# conda install pytorch==1.11.0 cpuonly -c pytorch
conda install pytorch==1.11.0 cudatoolkit=11.3 -c pytorch -y
pip install setuptools
# Finally move into the directory and install the dependencies
cd CLEAN/app/
python build.py install
git clone https://github.com/facebookresearch/esm.git
mkdir data/esm_data

