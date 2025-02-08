#!/bin/bash
# The base enzymetk env which works with most tools
conda create --name dgo python==3.11.8 -y
conda activate dgo
pip install -r reqs.txt
conda install pytorch::faiss-gpu 
conda install -c conda-forge pyarrow