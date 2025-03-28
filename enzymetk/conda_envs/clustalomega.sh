#!/bin/bash
# Install FastTree
wget http://www.clustal.org/omega/clustalo-1.2.4-Ubuntu-x86_64 -O clustalo
chmod +x clustalo
echo export PATH=$PATH:$PWD/bin >> ~/.bashrc 
source ~/.bashrc