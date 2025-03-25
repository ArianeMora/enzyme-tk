from step import Step
import pandas as pd
import numpy as np
from tempfile import TemporaryDirectory
from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem import rdChemReactions
import pandas as pd
import os
from rdkit.DataStructs import FingerprintSimilarity
from rdkit.Chem.Fingerprints import FingerprintMols
import random
import string
from tqdm import tqdm


class ReactionDist(Step):
    
    def __init__(self, id_column_name: str, smiles_column_name: str, smiles_string: str):
        self.smiles_column_name = smiles_column_name
        self.id_column_name = id_column_name
        self.smiles_string = smiles_string
        
    def __execute(self, data: list) -> np.array:
        reaction_df, tmp_dir = data
        tmp_label = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        
        rxn = rdChemReactions.ReactionFromSmarts(self.smiles_string)
        rxn_fp = rdChemReactions.CreateStructuralFingerprintForReaction(rxn)

        # make a list of fingerprints (fp) and molecules (ms)
        ms = [rdChemReactions.ReactionFromSmarts(x) for x in reaction_df[self.smiles_column_name].values]
        fps = [rdChemReactions.CreateStructuralFingerprintForReaction(x) for x in ms]
        rows = []
        smiles = reaction_df[self.smiles_column_name].values
        ids = reaction_df[self.id_column_name].values
        # compare all fp pairwise without duplicates
        for n in tqdm(range(len(fps))): # -1 so the last fp will not be used
            rows.append([ids[n], 
                         smiles[n], 
                         DataStructs.TanimotoSimilarity(fps[n], rxn_fp), 
                         DataStructs.FingerprintSimilarity(fps[n], rxn_fp),
                         DataStructs.RusselSimilarity(fps[n], rxn_fp), 
                         DataStructs.CosineSimilarity(fps[n], rxn_fp)])
        distance_df = pd.DataFrame(rows, columns=[self.id_column_name, 'TargetSmiles', 'TanimotoSimilarity', 'FingerprintSimilarity', 'RusselSimilarity', 'CosineSimilarity'])
        return distance_df
        
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
       return self.__execute([df, None])
