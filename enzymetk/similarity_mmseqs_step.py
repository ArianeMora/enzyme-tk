"""
Install clean and then you need to activate the environment and install and run via that. 

Honestly it's a bit hacky the way they do it, not bothered to change things so have to save the data to their
repo and then copy it out of it.
"""
from enzymetk.step import Step

import pandas as pd
import numpy as np
from tempfile import TemporaryDirectory
import subprocess
import random
import string


def process_clustering(filename, df, id_column_name):
    clustering = pd.read_csv(filename, delimiter='\t', header=None)
    #rename heading as cluster reference and id
    clustering.columns = ['mmseqs_representative_cluster_seq', id_column_name]
    clustering.drop_duplicates(subset=id_column_name, keep='first', inplace=True)
    clustering.set_index(id_column_name, inplace=True)
    # Join the clustering with the df
    df = df.set_index(id_column_name)
    df = df.join(clustering, how='left')
    df.reset_index(inplace=True)
    return df

class MMseqs(Step):
    
    def __init__(self, id_column_name: str, seq_column_name: str, method='search',reference_database: str = None, tmp_dir: str = None, args: list = None):
        self.seq_column_name = seq_column_name
        self.id_column_name = id_column_name
        self.reference_database = reference_database # pdb should be the default
        self.tmp_dir = tmp_dir
        self.args = args
        self.method = method
        
    def __execute(self, data: list) -> np.array:
        df, tmp_dir = data
        tmp_label = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        # Convert to a fasta
        with open(f'{tmp_dir}/seqs.fasta', 'w') as f:
            for i, row in df.iterrows():
                f.write(f'>{row[self.id_column_name]}\n{row[self.seq_column_name]}\n')
            
        if self.reference_database is None and self.method == 'search':
            print('Creating database')
            cmd = ['mmseqs', 'createdb', f'{tmp_dir}/seqs.fasta', 'targetDB']
            self.run(cmd)
            cmd = ['mmseqs', 'createindex', 'targetDB', 'tmp']
            self.run(cmd)
            self.reference_database = 'targetDB'

        # e.g. args --min-seq-id 0.5 -c 0.8 --cov-mode 1
        if self.method == 'search':
            cmd = ['mmseqs', 'easy-search', f'{tmp_dir}/seqs.fasta', self.reference_database, f'{tmp_dir}/{tmp_label}.txt', f'{tmp_dir}/tmp']
        elif self.method == 'cluster':
            cmd = ['mmseqs', 'easy-cluster', f'{tmp_dir}/seqs.fasta', f'{tmp_dir}/clusterRes', f'{tmp_dir}/tmp']
        # add in args
        if self.args is not None:
           cmd.extend(self.args)

        self.run(cmd)
        # https://github.com/soedinglab/MMseqs2/issues/458
        if self.method == 'search':
            df = pd.read_csv(f'{tmp_dir}/{tmp_label}.txt', header=None, sep='\t')
            df.columns = ['Query', 'Target', 'Sequence Identity', 'Alignment Length', 'Mismatches',  'Gap Opens', 
                          'Query Start', 'Query End', 'Target Start', 'Target End', 'E-value', 'Bit Score']
            return df
        elif self.method == 'cluster':
            df = process_clustering(f'{tmp_dir}/clusterRes_cluster.tsv', df, self.id_column_name)   
            return df
    
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.tmp_dir is not None:
            return self.__execute([df, self.tmp_dir])
        with TemporaryDirectory() as tmp_dir:
            return self.__execute([df, tmp_dir])
            return df