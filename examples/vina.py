import sys
sys.path.append('/disk1/ariane/vscode/enzyme-tk/')
from enzymetk.dock_vina_step import Vina
from enzymetk.save_step import Save
import pandas as pd
import os

rxn_smiles = 'CCCCC(COC(C1=CC=CC=C1C(OCC(CCCC)CC)=O)=O)CC>>O=C(O)C1=CC=CC=C1C(O)=O'

output_dir = 'tmp/'
num_threads = 1
id_col = 'Entry'
seq_col = 'Sequence'
substrate_col = 'Substrate'
rows = [['P0DP23', None, '1|2', 'TPP', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC'], 
        ['P0DP24', None, '2|3', 'TPP', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'O=C(OC(C)C)NC1=CC=CC(Cl)=C1']]
df = pd.DataFrame(rows, columns=[id_col, 'structure', 'residues', 'name', seq_col, substrate_col])
# self, id_col: str, structure_col: str, sequence_col: str,  substrate_col: str, substrate_name_col: str, active_site_col: str, output_dir: str, num_threads: in
df << (Vina(id_col, 'structure', seq_col, substrate_col, 'name', 'residues', 'tmp/', 2) >> Save(f'{output_dir}vina.pkl'))