import sys
sys.path.append('../enzymetk/')

from steps.annotateEC_CLEAN_step import CLEAN
from steps.save_step import Save
import pandas as pd

output_dir = 'tmp/'
num_threads = 1
id_col = 'Entry'
seq_col = 'Sequence'
substrate_col = 'Substrate'
rows = [['P0DP23', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC'], 
        ['P0DP24', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC']]
df = pd.DataFrame(rows, columns=[id_col, seq_col, substrate_col])

# This should be relative to the location of the script if you installed via the install_all.sh script
clean_dir = '/disk1/ariane/vscode/enzyme-tk/enzymetk/conda_envs/CLEAN/app/'
df << (CLEAN(id_col, seq_col, clean_dir, num_threads=1) >> Save(f'{output_dir}clean_test.pkl'))