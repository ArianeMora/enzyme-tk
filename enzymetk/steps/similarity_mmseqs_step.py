"""
Install clean and then you need to activate the environment and install and run via that. 

Honestly it's a bit hacky the way they do it, not bothered to change things so have to save the data to their
repo and then copy it out of it.
"""
from step import Step
import pandas as pd
import numpy as np
from tempfile import TemporaryDirectory
import subprocess
import random
import string


class MMseqs(Step):
    
    def __init__(self, pdb_column_name: str, reference_database: str, tmp_dir: str = None, args: list = None):
        self.pdb_column_name = pdb_column_name
        self.reference_database = reference_database # pdb should be the default
        self.tmp_dir = tmp_dir
        self.args = args
        
    def __execute(self, data: list) -> np.array:
        df, tmp_dir = data
        tmp_label = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        # Get the PDB files from the column
        pdb_files = list(df[self.pdb_column_name].values)
                
        subprocess.run(['foldseek', 'easy-search'] + pdb_files + [f'{self.reference_database}', f'{tmp_dir}{tmp_label}.txt', 'tmp'], check=True)
        
        df = pd.read_csv(f'{tmp_dir}{tmp_label}.txt', header=None, sep='\t')
        df.columns = ['Query', 'Target', 'Calpha coordinates of the query', 'Calpha coordinates of the target', 'TM-score of the alignment', 
                      'TM-score normalized by the query length', 'TM-score normalized by the target length', 'Rotation matrix (computed to by TM-score)', 
                      'Translation vector (computed to by TM-score)', 'Average LDDT of the alignment', 'LDDT per aligned position', 'Estimated probability for query and target to be homologous']
        
        return df
    
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.tmp_dir is not None:
            return self.__execute([df, self.tmp_dir])
        with TemporaryDirectory() as tmp_dir:
            return self.__execute([df, tmp_dir])
            return df