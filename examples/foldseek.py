import sys
sys.path.append('../enzymetk/')

from steps.similarity_foldseek_step import FoldSeek
from steps.save_step import Save
import pandas as pd


# id_col: str, seq_col: str, proteinfer_dir: str,
output_dir = 'tmp/'
rows = [['tmp/P0DP24/chai/P0DP24_3.cif'],
        ['tmp/P0DP24/chai/P0DP24_1.cif']]
df = pd.DataFrame(rows, columns=['pdbs'])
# foldseek_dir: str, pdb_column_name: str, reference_database: str
pdb_column_name = 'pdbs'
reference_database = '/disk1/share/software/foldseek/structures/pdb/pdb'
df << (FoldSeek(pdb_column_name, reference_database) >> Save(f'{output_dir}pdb_files.pkl'))
