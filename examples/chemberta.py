from enzymetk.embedchem_chemberta_step import ChemBERT
from enzymetk.save_step import Save
import pandas as pd
import os
os.environ['MKL_THREADING_LAYER'] = 'GNU'

output_dir = 'tmp/'
num_threads = 1
id_col = 'Entry'
seq_col = 'Sequence'
substrate_col = 'Substrate'
rows = [['P0DP23', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC'], 
        ['P0DP24', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC']]
df = pd.DataFrame(rows, columns=[id_col, seq_col, substrate_col])
df << (ChemBERT(id_col, substrate_col, num_threads) >> Save(f'{output_dir}chemberta.pkl'))
