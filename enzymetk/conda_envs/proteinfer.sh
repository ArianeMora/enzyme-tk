#!/bin/bash
# Proteinfer
conda create --name proteinfer -c conda-forge python=3.7.12 -y
conda activate proteinfer
pip3 install -r proteinfer_requirements.txt