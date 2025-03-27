#./foldseek easy-search /home/ariane/degradeo/data/pipeline/p1_predict_activity/p1b_encode_protein/e1_esm/chai/Q0HLQ7/chai/Q0HLQ7_0.cif /home/ariane/degradeo/data/pipeline/p1_predict_activity/p1b_encode_protein/e1_esm/chai/Q0HLQ7/chai/Q0HLQ7_1.cif pdb test_aln.fasta tmp
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


""" Install: conda install -c conda-forge -c bioconda -c defaults prokka """
class Prokka(Step):
    
    def __init__(self, porechop_dir: str, name: str, input_column_name: str, output_dir: str, num_threads=1):
        self.porechop_dir = porechop_dir
        self.name = name
        self.input_column_name = input_column_name
        self.output_dir = output_dir
        self.num_threads = num_threads
        
    def __execute(self, data: list) -> np.array:
        df = data
        # f'prokka --outdir {data_dir}prokka/{l} --prefix {l} {data_dir}flye/{l}/assembly.fasta ')
        file_created = []
        for name, input_filename, output_dir in df[[self.name, self.input_column_name, self.output_dir]]:    
            # Note it expects the input file name to be the outpt from flye
            subprocess.run([f'prokka', '--outdir', output_dir, '--prefix', name, input_filename], check=True)
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