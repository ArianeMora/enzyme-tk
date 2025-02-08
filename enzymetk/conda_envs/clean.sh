#!/bin/bash
# Clean
conda create -n clean python==3.10.4 -y
conda activate clean
pip install -r clean_requirements.txt
# If you have CPU you need to install the following:
# conda install pytorch==1.11.0 cpuonly -c pytorch
conda install pytorch==1.11.0 cudatoolkit=11.3 -c pytorch