"""
Step to run multiple sequence alignment with the Clustal Omega tool. 
 ./clustalo -i /home/helen/degradeo/pipeline/helen_data/sequences_test_fasta.txt
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

class ClustalOmega(Step):
    
    def __init__(self, clustalomega_dir: str, sequence_column_name: str):
        self.clustalomega_dir = clustalomega_dir
        self.sequence_column_name = sequence_column_name
        self.num_threads = 1

    def __execute(self, data: list) -> np.array: 
        df, tmp_dir = data
        tmp_label = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        fasta_file = os.path.join(tmp_dir, 'sequences.fasta')
        output_file = os.path.join(tmp_dir, f"{tmp_label}.aln")

        # Turn dataframe into fasta file
        with open(fasta_file, 'w') as f:
            for index, row in df.iterrows():
                f.write(f">{row['ID']}\n{row['sequence']}\n")

        # Running Clustal Omega on the generated FASTA file
        subprocess.run([f'{self.clustalomega_dir}./clustalo', '-i', fasta_file, '-o', output_file], check=True)

        sequences = {}

        # Read the output file
        with open(output_file, 'r') as f:
            current_id = None
            for line in f:
                line = line.strip()  # Remove leading/trailing whitespaces or newline characters
                if line.startswith(">"):
                    # Header line with sequence ID
                    current_id = line[1:]  # Extract ID without ">"
                    sequences[current_id] = ""  # Initialize an empty string for this ID
                else:
                    # Sequence line; append it to the current ID's sequence
                    sequences[current_id] += line

        # Convert the sequences dictionary into a DataFrame
        df_aligned = pd.DataFrame(list(sequences.items()), columns=['ID', 'aligned_sequence'])

        df = pd.merge(df, df_aligned, on='ID', how='left')
        #print(df.head())
                
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