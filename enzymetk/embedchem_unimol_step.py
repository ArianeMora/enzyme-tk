from enzymetk.step import Step
import pandas as pd
from tempfile import TemporaryDirectory
import logging
import numpy as np
from unimol_tools import UniMolRepr
from multiprocessing.dummy import Pool as ThreadPool

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# pip install unimol_tools


class UniMol(Step):
    
    def __init__(self, smiles_col: str, unimol_model = 'unimolv2', unimol_size = '164m', num_threads = 1):
        self.smiles_col = smiles_col
        self.num_threads = num_threads
        # single smiles unimol representation
        clf = UniMolRepr(data_type='molecule', 
                        remove_hs=False,
                        model_name= unimol_model or 'unimolv2', # avaliable: unimolv1, unimolv2
                        model_size= unimol_size or '164m', # work when model_name is unimolv2. avaliable: 84m, 164m, 310m, 570m, 1.1B.
                        )
        self.clf = clf

    def __execute(self, df: pd.DataFrame) -> pd.DataFrame:
        smiles_list = list(df[self.smiles_col].values)
        reprs = []
        for smile in smiles_list:
            try:
                unimol_repr = self.clf.get_repr([smile], return_atomic_reprs=True)
                reprs.append(unimol_repr['cls_repr'])
            except Exception as e:
                logger.warning(f"Error embedding smile {smile}: {e}")
                reprs.append(None)
        df['unimol_repr']  = reprs
        return df
    
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        with TemporaryDirectory() as tmp_dir:
            if self.num_threads > 1:
                data = []
                df_list = np.array_split(df, self.num_threads)
                for df_chunk in df_list:
                    data.append(df_chunk)
                pool = ThreadPool(self.num_threads)
                output_filenames = pool.map(self.__execute, data)
                df = pd.DataFrame()
                for tmp_df in output_filenames:
                    df = pd.concat([df, tmp_df])
                return df
            
            else:
                return self.__execute(df)
                