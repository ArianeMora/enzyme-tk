from enzymetk.step import Step
import pandas as pd
import numpy as np
from multiprocessing.dummy import Pool as ThreadPool
from transformers import AutoModel, AutoTokenizer

class ChemBERT(Step):
    
    def __init__(self, id_col: str, value_col: str, num_threads: int):
        self.id_col = id_col
        self.value_col = value_col
        self.num_threads = num_threads
        model_version = 'seyonec/PubChem10M_SMILES_BPE_450k'
        self.model = AutoModel.from_pretrained(model_version, output_attentions=True)
        self.tokenizer = AutoTokenizer.from_pretrained(model_version)
        self.seq_len_limit = 500
        self.embedding_len = 768
        
        
    def __execute(self, data: list) -> np.array:
        results = []
        for v in data:
            i, smiles = v[0], v[1]
            print(smiles)
            encoded_input = self.tokenizer(
                smiles,
                truncation=True,
                max_length=self.seq_len_limit,
                padding='max_length',
                return_tensors='pt')
            output = self.model(**encoded_input)
            results.append((i, output['last_hidden_state'][:, 0][0].detach().numpy())) 
        return results

    
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.num_threads > 1:
            data = []
            df_list = np.array_split(df, self.num_threads)
            pool = ThreadPool(self.num_threads)
            for df_chunk in df_list:
                data.append([(i, v) for i, v in df_chunk[[self.id_col, self.value_col]].values])
            results = pool.map(self.__execute, data)
            all_results_map = {}
            for r in results:
                for j in r:
                    all_results_map[j[0]] = j[1]
            encodings = []
            for uid in df[self.id_col].values:
                if all_results_map.get(uid) is None:
                    encodings.append(np.zeros(self.embedding_len))
                else:
                    encodings.append(all_results_map.get(uid))
            df['chemberta'] = encodings
            return df
        
        else:
            data = [(i, v) for i, v in df[[self.id_col, self.value_col]].values]
            results = self.__execute(data)
            df['chemberta'] = [r[1] for r in results]
            return df