from step import Step
import pandas as pd
from tempfile import TemporaryDirectory
import pickle
import subprocess
from pathlib import Path
import logging
import numpy as np
from tqdm import tqdm

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

    
class RxnFP(Step):
    
    def __init__(self, value_col: str, num_threads: int, bad_server=False):
        self.value_col = value_col
        self.num_threads = num_threads or 1
        self.bad_server = bad_server

    def __execute(self, df: pd.DataFrame, tmp_dir: str) -> pd.DataFrame:
        output_filename = f'{tmp_dir}/rxnfp.pkl'
        input_filename = f'{tmp_dir}/input.csv'
        df.to_csv(input_filename, index=False)
        # Might have an issue if the things are not correctly installed in the same dicrectory 
        result = subprocess.run(['conda', 'run', '-n', 'rxnfp', 'python', Path(__file__).parent/'embedchem_rxnfp_run.py', '--out', output_filename, 
                                '--input', input_filename, '--label', self.value_col], capture_output=True, text=True)
        if result.stderr:
            logger.error(result.stderr)
        logger.info(result.stdout)   
        
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
