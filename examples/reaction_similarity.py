import sys
sys.path.append('../enzymetk/')

from steps.similarity_reaction import ReactionDist
from steps.save_step import Save
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
df << (ReactionDist(id_col, substrate_col, rxn_smiles) >> Save(f'{output_dir}reaction_similarity.pkl'))