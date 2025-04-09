
import sys

from enzymetk.inpaint_ligandMPNN_step import LigandMPNN
from enzymetk.save_step import Save
import pandas as pd

# id_col: str, seq_col: str, proteinfer_dir: str,
# This needs to be the full path to the file since LigandMPNN requires the full path (otherwise it will save to the ligandmpnn directory)
output_dir = '/disk1/ariane/vscode/enzyme-tk/examples/tmp/'
# These have to be the full path to the file since LigandMPNN requires the full path.
rows = [['/disk1/ariane/vscode/enzyme-tk/examples/tmp/P0DP24/chai/P0DP24_3.cif'],
        ['/disk1/ariane/vscode/enzyme-tk/examples/tmp/P0DP24/chai/P0DP24_1.cif']]
df = pd.DataFrame(rows, columns=['pdbs'])
# foldseek_dir: str, pdb_column_name: str, reference_database: str
pdb_column_name = 'pdbs'
ligand_mpnn_dir = '/disk1/share/software/LigandMPNN/'
args = ['--fixed_residues', '"A19 A20 A21 A59 A60 A61 A90 A91 A92"', '--checkpoint_path_sc', f'{ligand_mpnn_dir}model_params/ligandmpnn_sc_v_32_002_16.pt']
df << (LigandMPNN(pdb_column_name, ligand_mpnn_dir, output_dir,args=args) >> Save(f'{output_dir}ligandmpnn_inpainted.pkl'))
