#!/bin/bash
# Metagenomics
conda create -n metagenomics -c conda-forge python=3.10.14 -y
conda install -c conda-forge -c bioconda -c defaults prokka
conda install -c conda-forge -c bioconda mmseqs2
git clone https://github.com/rrwick/Porechop.git
# Also install porechop
cd Porechop
make
./porechop-runner.py -h
# Add to path I guess
echo export PATH=$PATH:$PWD >> ~/.bashrc 
# Move back one before getting sratoolkit
cd ..
# Sratoolkit
wget https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/3.1.1/sratoolkit.3.1.1-ubuntu64.tar.gz
tar -vxzf sratoolkit.3.1.1-ubuntu64.tar.gz
echo export PATH=$PATH:$PWD/bin >> ~/.bashrc 

