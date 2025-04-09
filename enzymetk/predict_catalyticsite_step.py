from enzymetk.step import Step
import pandas as pd
from tempfile import TemporaryDirectory
import subprocess
from pathlib import Path
import logging
import numpy as np
from tqdm import tqdm
import random
import string

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

    
class ActiveSitePred(Step):
    
    def __init__(self, id_col: str, seq_col: str, squidly_dir: str, num_threads: int = 1, 
                 esm2_model = 'esm2_t36_3B_UR50D', tmp_dir: str = None):
        self.id_col = id_col
        self.seq_col = seq_col  
        self.num_threads = num_threads or 1
        self.squidly_dir = squidly_dir
        self.esm2_model = esm2_model
        self.tmp_dir = tmp_dir

    def __to_fasta(self, df: pd.DataFrame, tmp_dir: str):
        tmp_label = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        input_filename = f'{tmp_dir}/as_inference_{tmp_label}.fasta'
        # Save as a fasta
        with open(input_filename, 'w+') as fout:
            for entry, seq in df[[self.id_col, self.seq_col]].values:
                fout.write(f'>{entry.strip()}\n{seq.strip()}\n')
        return input_filename
            
    def __execute(self, df: pd.DataFrame, tmp_dir: str):
        input_filename = self.__to_fasta(df, tmp_dir)
        # Might have an issue if the things are not correctly installed in the same dicrectory 
        result = subprocess.run(['python', Path(__file__).parent/'predict_catalyticsite_run.py', '--out', str(tmp_dir), 
                                '--input', input_filename, '--squidly_dir', self.squidly_dir, '--esm2_model', self.esm2_model], capture_output=True, text=True)
        output_filename = f'{input_filename.replace(".fasta", "_results.pkl")}'
        if result.stderr:
            logger.error(result.stderr)
        logger.info(result.stdout)   
        
        return output_filename
    
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        with TemporaryDirectory() as tmp_dir:
            tmp_dir = self.tmp_dir if self.tmp_dir is not None else tmp_dir
            if self.num_threads > 1:
                output_filenames = []
                df_list = np.array_split(df, self.num_threads)
                for df_chunk in tqdm(df_list):
                    try:
                        output_filenames.append(self.__execute(df_chunk, tmp_dir))
                    except Exception as e:
                         logger.error(f"Error in executing ESM2 model: {e}")
                         continue
                df = pd.DataFrame()
                print(output_filenames)
                for p in output_filenames:
                    sub_df = pd.read_pickle(p)
                    df = pd.concat([df, sub_df])
                return df
            
            else:
                output_filename = self.__execute(df, tmp_dir)
                return pd.read_pickle(output_filename)
