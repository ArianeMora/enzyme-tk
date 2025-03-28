# /home/ikumi/degradeo/software/FastTree -gtr -nt /home/ikumi/degradeo/pipeline/ikumi_data/Q04457_esterase-2.msa > /home/ikumi/degradeo/pipeline/ikumi_data/output_tree.tree
# /home/ikumi/degradeo/software/FastTree -wag /home/ikumi/degradeo/pipeline/ikumi_data/Q04457_esterase-2.msa > /home/ikumi/degradeo/pipeline/ikumi_data/output_tree.tree
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

class FastTree(Step):
    def __init__(self, fasttree_dir: str, id_col: str, seq_col: str, csv_file: str, output_dir: str):
        self.fasttree_dir = fasttree_dir
        self.id_col = id_col
        self.seq_col = seq_col
        self.csv_file = csv_file
        self.num_threads = 1
        self.output_dir = output_dir

    def create_alignment_file(self, df: pd.DataFrame) -> str:
        print(f"Creating MSA file from {len(df)} sequences")
        
        # Create MSA file in the output directory
        msa_file = os.path.join(self.output_dir, 'ikumi.data.msa')
        with open(msa_file, 'w') as fout:
            for entry, seq in df[[self.id_col, self.seq_col]].values:
                fout.write(f">{entry.strip()}\n{seq.strip()}\n")
                
        print(f"Created MSA file at: {msa_file}")
        return msa_file
    
    def __execute(self, data: list) -> pd.DataFrame:
        df, tmp_dir = data
        tmp_label = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        # Get the msa file
        msa_file = self.create_alignment_file(df)

        fasttree_executable = os.path.join(self.fasttree_dir, 'FastTree')
        output_tree_file = os.path.join(tmp_dir, f'{tmp_label}.tree')
        
        # Run FastTree and redirect output to a file
        with open(output_tree_file, 'w') as outfile:
            subprocess.run([fasttree_executable, '-wag', msa_file], stdout=outfile, check=True)
        
        df = pd.read_csv(output_tree_file, header=None, sep='\t')
        
        print(df.head())
        
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