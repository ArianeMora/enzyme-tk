"""
Step to run multiple sequence alignment with the Clustal Omega tool. 
 ./clustalo -i /home/helen/degradeo/pipeline/helen_data/sequences_test_fasta.txt
"""
from enzymetk.step import Step
import logging

import pandas as pd
import numpy as np
from multiprocessing.dummy import Pool as ThreadPool
from tempfile import TemporaryDirectory
import os
import subprocess
import random
import string
from tqdm import tqdm 


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class BLAST(Step):
    
    def __init__(self, id_col: str, sequence_col: str, label_col=None, database=None,
                 mode='blastp', args=None, tmp_dir=None, num_threads=1):
        self.id_col = id_col
        self.seq_col = sequence_col
        self.label_col = label_col  # This is whether it is query or reference
        self.mode = mode
        self.database = database
        self.args = args
        self.tmp_dir = tmp_dir
        self.num_threads = num_threads
        if self.database is None and self.label_col is None:
            raise ValueError('Database is not set, you can pass a database that you have already created see diamond for more information or the sequences \
                             as part of your dataframe and pass the label column (this needs to have two values: reference and query) reference \
                             refers to sequences that you want to search against and query refers to sequences that you want to search for.')
        
    def __execute(self, data: list) -> np.array: 
        df, tmp_dir = data
        tmp_label = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        query_fasta = os.path.join(tmp_dir, f'{tmp_label}_query.fasta')
        ref_fasta = os.path.join(tmp_dir, f'{tmp_label}_ref.fasta')
        db_label = os.path.join(tmp_dir, f'{tmp_label}_db')
        # write fasta file which is the input for proteinfer
        if self.label_col is not None:
            with open(query_fasta, 'w+') as fout:
                query_df = df[df[self.label_col] == 'query']
                print(query_df)
                for entry, seq in query_df[[self.id_col, self.seq_col]].values:
                    fout.write(f'>{entry.strip()}\n{seq.strip()}\n')

            with open(ref_fasta, 'w+') as fout:
                query_df = df[df[self.label_col] == 'reference']
                print(query_df)
                for entry, seq in query_df[[self.id_col, self.seq_col]].values:
                    fout.write(f'>{entry.strip()}\n{seq.strip()}\n')
            # Make the DB first 
            db_label = os.path.join(tmp_dir, f'{tmp_label}_refdb')
            subprocess.run(['diamond', 'makedb', '--in', ref_fasta, '-d', db_label], check=True)
        else:
            with open(query_fasta, 'w+') as fout:
                for entry, seq in df[[self.id_col, self.seq_col]].values:
                    fout.write(f'>{entry.strip()}\n{seq.strip()}\n')
            if os.path.exists(self.database):
                # Here we're assuming they're passing a database as a fasta file
                subprocess.run(['diamond', 'makedb', '--in', self.database, '-d', db_label], check=True)
            else:
                db_label = self.database
            
        # Running Clustal Omega on the generated FASTA file
        matches_filename = os.path.join(tmp_dir, f'{tmp_label}_matches.tsv')
        cmd = ['diamond', self.mode]
        if self.args is not None:
            cmd.extend(self.args)
        cmd.extend(['-d', db_label, '-q', query_fasta, '-o', matches_filename])
        print(cmd)
        self.run(cmd)
        df = pd.read_csv(matches_filename, sep='\t', header=None)
        print(df)
        df.columns = ['query', 'target', 'sequence identity', 'length', 'mismatch', 'gapopen', 'query start', 'query end', 'target start', 'target end', 'e-value', 'bitscore']
        return df

    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        with TemporaryDirectory() as tmp_dir:
            tmp_dir = self.tmp_dir if self.tmp_dir is not None else tmp_dir
            if self.num_threads > 1:
                output_filenames = []
                df_list = np.array_split(df, self.num_threads)
                for df_chunk in tqdm(df_list):
                    try:
                        output_filenames.append(self.__execute([df_chunk, tmp_dir]))
                    except Exception as e:
                         logger.error(f"Error in executing ESM2 model: {e}")
                         continue
                df = pd.DataFrame()
                for sub_df in output_filenames:
                    df = pd.concat([df, sub_df])
                return df
            
            else:
                return self.__execute([df, tmp_dir])
            
    # def execute(self, df: pd.DataFrame) -> pd.DataFrame:
    #     if self.tmp_dir is not None:
    #         return self.__execute([df, self.tmp_dir])
    #     with TemporaryDirectory() as tmp_dir:
    #         return self.__execute([df, tmp_dir])
