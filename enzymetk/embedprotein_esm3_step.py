# ESM 3 script
from esm.sdk.api import ESMProtein
from tempfile import TemporaryDirectory
import torch
import os
import pandas as pd
from esm.models.esm3 import ESM3
from esm.sdk.api import ESMProtein, SamplingConfig
from huggingface_hub import login
from enzymetk.step import Step
import numpy as np
from tqdm import tqdm 

# CUDA setup
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"   # see issue #152
cuda = True
DEVICE = torch.device("cuda" if cuda else "cpu")
device = DEVICE 


class EmbedESM3(Step):
    
    def __init__(self, id_col: str, seq_col: str, extraction_method='mean', num_threads=1, 
                 tmp_dir: str = None, env_name: str = 'enzymetk', save_tensors=False): # type: ignore
        login()
        self.client = ESM3.from_pretrained("esm3-open").to("cuda")
        self.seq_col = seq_col
        self.id_col = id_col
        self.num_threads = num_threads or 1
        self.extraction_method = extraction_method
        self.tmp_dir = tmp_dir
        self.env_name = env_name
        self.save_tensors = save_tensors

    def __execute(self, df: pd.DataFrame, tmp_dir: str) -> pd.DataFrame: 
        client = self.client
        means = []
        for id, seq in tqdm(df[[self.id_col, self.seq_col]].values):
            protein = ESMProtein(
                sequence=(
                    seq
                )
            )
            protein_tensor = client.encode(protein)
            output = client.forward_and_sample(
                protein_tensor, SamplingConfig(return_per_residue_embeddings=True)
            )
            if self.save_tensors:
                torch.save(output.per_residue_embedding, os.path.join(tmp_dir, f'{id}.pt'))
            means.append(np.array(output.per_residue_embedding.mean(dim=0).cpu()))
        df['esm3_mean']  = means
        return df
    
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.tmp_dir is None:
            with TemporaryDirectory() as tmp_dir:
                if self.num_threads > 1:
                    dfs = []
                    df_list = np.array_split(df, self.num_threads)
                    for df_chunk in tqdm(df_list):
                        dfs.append(self.__execute(df_chunk, tmp_dir))
                    df = pd.DataFrame()
                    for tmp_df in tqdm(dfs):
                        df = pd.concat([df, tmp_df])
                    return df
                else:
                    df = self.__execute(df, tmp_dir)
                    return df
        else:
            df = self.__execute(df, self.tmp_dir)
            return df
