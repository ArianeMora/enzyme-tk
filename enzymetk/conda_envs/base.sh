#!/bin/bash
# The base enzymetk env which works with most tools
conda create --name enzymetk python==3.11.8 -y
conda activate enzymetk
pip install -r base_requirements.txt
conda install pytorch::faiss-gpu 
conda install -c conda-forge pyarrow