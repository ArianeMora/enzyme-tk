from enzymetk.step import Step
import pandas as pd
from docko.chai import run_chai
import logging
import numpy as np


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

    
class Chai(Step):
    
    def __init__(self, id_col: str, seq_col: str, substrate_col: str, output_dir: str, num_threads: int):
        self.id_col = id_col
        self.seq_col = seq_col
        self.substrate_col = substrate_col
        self.output_dir = output_dir or None
        self.num_threads = num_threads or 1

    def __execute(self, df: pd.DataFrame, tmp_dir: str) -> pd.DataFrame:
        output_filenames = []
        for run_id, seq, substrate in df[[self.id_col, self.seq_col, self.substrate_col]].values:
            # Might have an issue if the things are not correctly installed in the same dicrectory 
            if not isinstance(substrate, str):
                substrate = ''
            print(run_id, seq, substrate)
            run_chai(run_id, # name
                    seq, # sequence
                    substrate, # ligand as smiles
                    tmp_dir)
            output_filenames.append(f'{tmp_dir}/{run_id}/')
        return output_filenames
    
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.output_dir:
            if self.num_threads > 1:
                output_filenames = []
                df_list = np.array_split(df, self.num_threads)
                for df_chunk in df_list:
                    output_filenames += self.__execute(df_chunk, self.output_dir)
                    
                df['output_dir'] = output_filenames
                return df
            
            else:
                output_filenames = self.__execute(df, self.output_dir)
                df['output_dir'] = output_filenames
                return df
        else:
            print('No output directory provided')