#./foldseek easy-search /home/ariane/degradeo/data/pipeline/p1_predict_activity/p1b_encode_protein/e1_esm/chai/Q0HLQ7/chai/Q0HLQ7_0.cif /home/ariane/degradeo/data/pipeline/p1_predict_activity/p1b_encode_protein/e1_esm/chai/Q0HLQ7/chai/Q0HLQ7_1.cif pdb test_aln.fasta tmp
"""
Install clean and then you need to activate the environment and install and run via that. 

Honestly it's a bit hacky the way they do it, not bothered to change things so have to save the data to their
repo and then copy it out of it.
"""
from step import Step
import pandas as pd
import numpy as np
from multiprocessing.dummy import Pool as ThreadPool
from tempfile import TemporaryDirectory
import os
import subprocess
import random
import string


class FoldSeek(Step):
    
    def __init__(self, foldseek_dir: str, pdb_column_name: str, reference_database: str, num_threads: int):
        self.foldseek_dir = foldseek_dir
        self.pdb_column_name = pdb_column_name
        self.reference_database = reference_database # pdb should be the default
        self.num_threads = num_threads
        
    def __execute(self, data: list) -> np.array:
        df, tmp_dir = data
        tmp_label = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        # Get the PDB files from the column
        pdb_files = list(df[self.pdb_column_name].values)
        
        print([f'{self.foldseek_dir}foldseek', 'easy-search'] + pdb_files + [f'{self.reference_database}', f'{tmp_dir}{tmp_label}.txt', 'tmp'])
        
        subprocess.run([f'{self.foldseek_dir}foldseek', 'easy-search'] + pdb_files + [f'{self.reference_database}', f'{tmp_dir}{tmp_label}.txt', 'tmp'], check=True)
        
        df = pd.read_csv(f'{tmp_dir}{tmp_label}.txt', header=None, sep='\t')
        
        print(df.head())
        
        return df
    
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        with TemporaryDirectory() as tmp_dir:
            if self.num_threads > 1:
                data = []
                df_list = np.array_split(df, self.num_threads)
                pool = ThreadPool(self.num_threads)
                for df_chunk in df_list:
                    data.append([df_chunk, tmp_dir])
                results = pool.map(self.__execute, data)
                df = pd.DataFrame()
                for dfs in results:
                    df = pd.concat([df, dfs])
                return df
            else:
                return self.__execute([df, tmp_dir])
                return df