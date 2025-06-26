from enzymetk.step import Step
import pandas as pd
from docko.boltz import run_boltz_affinity
import logging
import numpy as np
from multiprocessing.dummy import Pool as ThreadPool


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

    
class Boltz(Step):
    
    def __init__(self, id_col: str, seq_col: str, substrate_col: str, intermediate_col: str, output_dir: str, num_threads: int):
        self.id_col = id_col
        self.seq_col = seq_col
        self.substrate_col = substrate_col
        self.intermediate_col = intermediate_col
        self.output_dir = output_dir or None
        self.num_threads = num_threads or 1

    def __execute(self, df: pd.DataFrame) -> pd.DataFrame:
        output_filenames = []
        
        for run_id, seq, substrate, intermediate in df[[self.id_col, self.seq_col, self.substrate_col, self.intermediate_col]].values:
            # Might have an issue if the things are not correctly installed in the same dicrectory 
            if not isinstance(substrate, str):
                substrate = ''
            print(run_id, seq, substrate)
            run_boltz_affinity(run_id, seq, substrate, self.output_dir, intermediate)
            output_filenames.append(f'{self.output_dir}/{run_id}/')
        return output_filenames
    
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.output_dir:
            if self.num_threads > 1:
                pool = ThreadPool(self.num_threads)
                df_list = np.array_split(df, self.num_threads)
                results = pool.map(self.__execute, df_list)
            else:
                results = self.__execute(df)
            df['output_dir'] = results
            return df
        else:
            print('No output directory provided')