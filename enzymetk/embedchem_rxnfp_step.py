from enzymetk.step import Step
import pandas as pd
from tempfile import TemporaryDirectory
import pickle
import subprocess
from pathlib import Path
import logging
import numpy as np
from tqdm import tqdm
import random
import string

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

    
class RxnFP(Step):
    
    def __init__(self, smiles_col: str, num_threads: int, env_name: str = 'rxnfp'):
        self.value_col = smiles_col
        self.num_threads = num_threads or 1
        self.env_name = env_name

    def __execute(self, df: pd.DataFrame, tmp_dir: str) -> pd.DataFrame:
        tmp_label = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        output_filename = f'{tmp_dir}/rxnfp_{tmp_label}.pkl'
        input_filename = f'{tmp_dir}/input_{tmp_label}.csv'
        df.to_csv(input_filename, index=False)
        cmd = ['conda', 'run', '-n', self.env_name, 'python', Path(__file__).parent/'embedchem_rxnfp_run.py', '--out', output_filename, 
                                '--input', input_filename, '--label', self.value_col]
        self.run(cmd)
        # Might have an issue if the things are not correctly installed in the same dicrectory 
        
        return output_filename
    
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        with TemporaryDirectory() as tmp_dir:
            if self.num_threads > 1:
                output_filenames = []
                df_list = np.array_split(df, self.num_threads)
                for df_chunk in tqdm(df_list, total=len(df_list)):
                    output_filenames.append(self.__execute(df_chunk, tmp_dir))
                    
                df = pd.DataFrame()
                for p in output_filenames:
                    with open(f'{p}', 'rb') as file:
                        tmp_df = pickle.load(file)
                    df = pd.concat([df, tmp_df])
                return df
            
            else:
                output_filename = self.__execute(df, tmp_dir)
                with open(f'{output_filename}', 'rb') as file:
                    return pickle.load(file)
