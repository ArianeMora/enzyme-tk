"""
Install clean and then you need to activate the environment and install and run via that. 

Honestly it's a bit hacky the way they do it, not bothered to change things so have to save the data to their
repo and then copy it out of it.
"""
from enzymetk.step import Step
import pandas as pd
import numpy as np
from multiprocessing.dummy import Pool as ThreadPool
from tempfile import TemporaryDirectory
import os
import subprocess
import random
import string


class PoreChop(Step):
    
    def __init__(self, porechop_dir: str, input_column_name: str, output_column_name: str, num_threads=1):
        self.porechop_dir = porechop_dir
        self.input_column_name = input_column_name
        self.output_column_name = output_column_name
        self.num_threads = num_threads
        
    def __execute(self, data: list) -> np.array:
        df = data
        # f'./porechop-runner.py -i {data_dir}fastq/{l}.fastq -o {data_dir}trimmed/{l}.fastq'  
        file_created = []
        for input_filename, output_filename in df[[self.input_column_name, self.output_column_name]]:        
            subprocess.run([f'{self.porechop_dir}./porechop-runner.py', '-i',  input_filename, '-o', output_filename], check=True)
            # Check that the file was created 
            if os.path.exists(output_filename):
                file_created.append(True)
            else:
                file_created.append(False)
        df['file_created'] = file_created
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