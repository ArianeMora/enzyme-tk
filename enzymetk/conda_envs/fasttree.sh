#!/bin/bash
wget https://morgannprice.github.io/fasttree/FastTree -O FastTree
chmod +x FastTree
echo export PATH=$PATH:$PWD/bin >> ~/.bashrc 
source ~/.bashrc