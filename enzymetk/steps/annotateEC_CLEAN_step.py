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


class CLEAN(Step):
    
    def __init__(self, id_col: str, seq_col: str, clean_dir: str, num_threads: int = 1, 
                 ec1_filter: list = None, ec2_filter: list = None, ec3_filter: list = None, ec4_filter: list = None):
        self.id_col = id_col
        self.clean_dir = clean_dir
        self.seq_col = seq_col # This is the column which has the sequence in it 
        self.num_threads = num_threads  
        self.ec1_filter = ec1_filter        
        self.ec2_filter = ec2_filter
        self.ec3_filter = ec3_filter
        self.ec4_filter = ec4_filter

    def __filter_df(self, df: pd.DataFrame) -> pd.DataFrame:
        # ------------- Separate out ECs ------------------
        df['id'] = [c.split(',')[0] for c in df[0].values]
        df['ec'] = [c.split(',')[1:] for c in df[0].values]
        df = df.drop(columns=0)
        df = df.explode('ec')
        df['score'] = [float(ec.split('/')[1]) for ec in df['ec'].values]
        df['ec'] = [str(ec.split('/')[0]) for ec in df['ec'].values]
        df['predicted_ecs'] = [ec.split(':')[1] for ec in df['ec'].values]
        df['EC1'] = [r.split('.')[0] for r in df['predicted_ecs'].values]
        df['EC2'] = [r.split('.')[1] for r in df['predicted_ecs'].values]
        df['EC3'] = [r.split('.')[2] for r in df['predicted_ecs'].values]
        df['EC4'] = [r.split('.')[3] for r in df['predicted_ecs'].values]
        
        if self.ec1_filter is not None:
            df = df[df['EC1'].isin(self.ec1_filter)]
        if self.ec2_filter is not None:
            df = df[df['EC2'].isin(self.ec2_filter)]
        if self.ec3_filter is not None:
            df = df[df['EC3'].isin(self.ec3_filter)]
        if self.ec4_filter is not None:
            df = df[df['EC4'].isin(self.ec4_filter)]
            
        df = df.sort_values(by='score', ascending=False)
        # Drop duplicates based on id only keeping the highest score
        df.drop_duplicates(subset='id', keep='first', inplace=True)
        return df
    
    def __execute(self, data: list) -> np.array:
        df, tmp_dir = data
        # Make sure in the directory of proteinfer
        # Create the fasta file based on the id and the sequence value columns
        tmp_label = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        input_filename = f'{tmp_dir}CLEAN_{tmp_label}.fasta'
        
        # write fasta file which is the input for proteinfer
        with open(input_filename, 'w+') as fout:
            for entry, seq in df[[self.id_col, self.seq_col]].values:
                fout.write(f'>{entry.strip()}\n{seq.strip()}\n')
        # Run it multi threaded
        os.chdir(self.clean_dir)

        tmp_label = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        # Since clean is GPU hungry, we only run CLEAN on the ones that proteInfer has predicted to be class 3.
        # Need to first copy the data to the CLEAN folder because it's stupid
        subprocess.run(['cp',  input_filename, f'{self.clean_dir}data/inputs/{tmp_label}.fasta'], check=True)
        # Run clean with clean environment
        subprocess.run(['conda', 'run', '-n', 'clean', 'python3', f'{self.clean_dir}CLEAN_infer_fasta.py', 
                        '--fasta_data', tmp_label], check=True)
        # Copy across the results file
        df = pd.read_csv(f'{self.clean_dir}results/inputs/{tmp_label}_maxsep.csv', header=None, sep='\t')
        # Clean up
        subprocess.run(['rm', f'{self.clean_dir}data/inputs/{tmp_label}.fasta'])
        subprocess.run(['rm', f'{self.clean_dir}results/inputs/{tmp_label}_maxsep.csv'])
        
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