import sys

from enzymetk.annotateEC_proteinfer_step import ProteInfer
from enzymetk.save_step import Save
import pandas as pd
import os

rxn_smiles = 'CCCCC(COC(C1=CC=CC=C1C(OCC(CCCC)CC)=O)=O)CC>>O=C(O)C1=CC=CC=C1C(O)=O'

output_dir = 'tmp/'
num_threads = 1
id_col = 'Entry'
seq_col = 'Sequence'
substrate_col = 'Substrate'
rows = [['P0DP23', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC>>O=C(O)C1=CC=CC=C1C(O)=O'], 
        ['P0DP24', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'O=C(OC(C)C)NC1=CC=CC(Cl)=C1>>O=C(O)C1=CC=CC=C1C(O)=O']]
df = pd.DataFrame(rows, columns=[id_col, seq_col, substrate_col])
df << (ProteInfer(id_col, seq_col, proteinfer_dir='/disk1/ariane/vscode/enzyme-tk/enzymetk/conda_envs/proteinfer/') >> Save('/disk1/ariane/vscode/enzyme-tk/examples/proteinfer.pkl'))