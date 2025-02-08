#!/bin/bash
conda create -n ligandmpnn_env python=3.11 -y
conda activate ligandmpnn_env
pip3 install -r ligandmpnn_requirements.txt