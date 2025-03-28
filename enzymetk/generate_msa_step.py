"""
Step to run multiple sequence alignment with the Clustal Omega tool. 
 ./clustalo -i /home/helen/degradeo/pipeline/helen_data/sequences_test_fasta.txt
"""
from enzymetk.step import Step
import pandas as pd
import numpy as np
from tempfile import TemporaryDirectory
import os
import subprocess
import random
import string

class ClustalOmega(Step):
    
    def __init__(self, id_col: str, seq_col: str, tmp_dir: str = None):
        self.seq_col = seq_col
        self.id_col = id_col
        self.tmp_dir = tmp_dir

    def __execute(self, data: list) -> np.array: 
        df, tmp_dir = data
        tmp_label = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        fasta_file = os.path.join(tmp_dir, 'sequences.fasta')
        output_file = os.path.join(tmp_dir, f"{tmp_label}.aln")

        # Turn dataframe into fasta file
        with open(fasta_file, 'w') as f:
            for seq_id, seq in df[[self.id_col, self.seq_col]].values:
                f.write(f">{seq_id}\n{seq}\n")

        # Running Clustal Omega on the generated FASTA file
        subprocess.run(['clustalo', '-i', fasta_file, '-o', output_file], check=True)

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
                    sequences[current_id] += line.strip()

        # Convert the sequences dictionary into a DataFrame
        df_aligned = pd.DataFrame(list(sequences.items()), columns=[self.id_col, 'aligned_sequence'])

        df = pd.merge(df, df_aligned, on=self.id_col, how='left')
                
        return df

    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.tmp_dir is not None:
            return self.__execute([df, self.tmp_dir])
        with TemporaryDirectory() as tmp_dir:
            return self.__execute([df, tmp_dir])