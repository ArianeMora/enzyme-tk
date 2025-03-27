from enzymetk.step import Step
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
from multiprocessing.dummy import Pool as ThreadPool


class SubstrateDist(Step):
    
    def __init__(self, id_column_name: str, smiles_column_name: str, smiles_string: str, num_threads=1):
        self.smiles_column_name = smiles_column_name
        self.id_column_name = id_column_name
        self.smiles_string = smiles_string
        self.num_threads = num_threads
        
    def __execute(self, data: list) -> np.array:
        reaction_df = data
        tmp_label = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        
        rxn = Chem.MolFromSmiles(self.smiles_string)
        rxn_fp = FingerprintMols.FingerprintMol(rxn)
        rows = []
        # compare all fp pairwise without duplicates
        for smile_id, smiles in tqdm(reaction_df[[self.id_column_name, self.smiles_column_name]].values): # -1 so the last fp will not be used
            mol_ = Chem.MolFromSmiles(smiles)
            fps = FingerprintMols.FingerprintMol(mol_)
            rows.append([smile_id, 
                         smiles, 
                         DataStructs.TanimotoSimilarity(fps, rxn_fp), 
                         DataStructs.RusselSimilarity(fps, rxn_fp), 
                         DataStructs.CosineSimilarity(fps, rxn_fp)])
        distance_df = pd.DataFrame(rows, columns=[self.id_column_name, 'TargetSmiles', 'TanimotoSimilarity', 'RusselSimilarity', 'CosineSimilarity'])
        return distance_df
        
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.num_threads > 1:
            data = []
            df_list = np.array_split(df, self.num_threads)
            for df_chunk in df_list:
                data.append(df_chunk)
            pool = ThreadPool(self.num_threads)
            output_filenames = pool.map(self.__execute, data)
            df = pd.DataFrame()
            for tmp_df in output_filenames:
                df = pd.concat([df, tmp_df])
            return df
        
        else:
            return self.__execute(df)
