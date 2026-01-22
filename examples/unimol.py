from enzymetk.embedchem_unimol_step import UniMol
from enzymetk.save_step import Save
import pandas as pd
import os
os.environ['MKL_THREADING_LAYER'] = 'GNU'

output_dir = 'tmp/'
num_threads = 1
id_col = 'Entry'
substrate_col = 'Substrate'
rows = [['P0DP23', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC'], 
        ['P0DP24', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC']]
df = pd.DataFrame(rows, columns=[id_col, substrate_col])
df << (UniMol(substrate_col, num_threads=num_threads) >> Save(f'{output_dir}unimol.pkl'))
