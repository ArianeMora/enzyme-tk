from step import Step
import pandas as pd
from tempfile import TemporaryDirectory
import pickle
import subprocess
from pathlib import Path
import logging
import numpy as np
import os
from tqdm import tqdm 
import torch

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

    
# First run this: nohup python esm-extract.py esm2_t33_650M_UR50D /disk1/ariane/vscode/degradeo/data/DEHP/uniprot/EC3.1.1_training.fasta /disk1/ariane/vscode/degradeo/data/DEHP/uniprot/encodings --include per_tok & 
def extract_mean_embedding(df, id_column, encoding_dir, rep_num=33): 
    """ Expects that the entries for the active site df are saved as the filenames in the encoding dir. """
    tensors = []
    files = os.listdir(encoding_dir)
    count_fail = 0
    count_success = 0
    for entry in tqdm(df[id_column].values):
        file = Path(encoding_dir + f'{entry}.pt')
        #try:
        embedding_file = torch.load(file)
        tensor = embedding_file['representations'][rep_num] # have to get the last layer (36) of the embeddings... very dependant on ESM model used! 36 for medium ESM2
        label = embedding_file['label']
        t = np.mean(np.asarray(tensor).astype(np.float32), axis=0)
        tensors.append(t)
        #f'--------------------- {entry} --------------')

    df['embedding'] = tensors
    # with open(f'{output_filename}', 'wb') as file:
    #     pickle.dump(df, file)
    print(count_success, count_fail, count_fail + count_success)
    return df

class EmbedESM(Step):
    
    def __init__(self, id_col: str, seq_col: str, extraction_method='mean', num_threads=1):
        self.seq_col = seq_col
        self.id_col = id_col
        self.num_threads = num_threads or 1
        self.extraction_method = extraction_method

    def __execute(self, df: pd.DataFrame, tmp_dir: str) -> pd.DataFrame:
        output_filename = f'{tmp_dir}/esm.pkl'
        input_filename = f'{tmp_dir}input.fasta'
        # write fasta file which is the input for proteinfer
        with open(input_filename, 'w+') as fout:
            for entry, seq in df[[self.id_col, self.seq_col]].values:
                fout.write(f'>{entry.strip()}\n{seq.strip()}\n')
        # Might have an issue if the things are not correctly installed in the same dicrectory 
        result = subprocess.run(['python', Path(__file__).parent/'esm-extract.py', 'esm2_t33_650M_UR50D', input_filename, tmp_dir, '--include per_tok'], capture_output=True, text=True)
        df = extract_mean_embedding(df, self.id_col, tmp_dir)
        if result.stderr:
            logger.error(result.stderr)
        logger.info(result.stdout)   
        
        return df
    
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        with TemporaryDirectory() as tmp_dir:
            if self.num_threads > 1:
                dfs = []
                df_list = np.array_split(df, self.num_threads)
                for df_chunk in df_list:
                    dfs.append(self.__execute(df_chunk, tmp_dir))
                df = pd.DataFrame()
                for tmp_df in dfs:
                    df = pd.concat([df, tmp_df])
                return df
            
            else:
                df = self.__execute(df, tmp_dir)
                return df
