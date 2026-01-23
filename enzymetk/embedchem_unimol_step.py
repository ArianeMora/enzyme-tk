import pandas as pd
from tempfile import TemporaryDirectory
import logging
import numpy as np
from enzymetk.step import Step

from multiprocessing.dummy import Pool as ThreadPool

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UniMol(Step):
    
    def __init__(self, smiles_col: str, unimol_model = 'unimolv2', 
                 unimol_size = '164m', num_threads = 1,
                 env_name = 'enzymetk', venv_name = None):
        super().__init__()
        self.smiles_col = smiles_col
        self.num_threads = num_threads
        self.conda = env_name
        self.env_name = env_name
        self.venv = venv_name if venv_name else f'{env_name}/bin/python'
        self.unimol_model = unimol_model
        self.unimol_size = unimol_size
        
 
    def install(self, env_args=None):
        # e.g. env args could by python=='3.1.1.
        self.install_venv(env_args)
        # Now the specific
        try:
            cmd = [f'{self.env_name}/bin/pip', 'install', 'unimol_tools']
            self.run(cmd)
        except Exception as e:
            cmd = [f'{self.env_name}/bin/pip3', 'install', 'unimol_tools']
            self.run(cmd)
        self.run(cmd)
        # Now set the venv to be the location:
        self.venv = f'{self.env_name}/bin/python'

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
        try:
            from unimol_tools import UniMolRepr
        except ImportError as e:
            raise ImportError(
                "UniMolRepr requires unimol-tools. "
                "Install after initializing class with install()"
            ) from e
        # single smiles unimol representation
        clf = UniMolRepr(data_type='molecule', 
                        remove_hs=False,
                        model_name= self.unimol_model or 'unimolv2', # avaliable: unimolv1, unimolv2
                        model_size= self.unimol_size or '164m', # work when model_name is unimolv2. avaliable: 84m, 164m, 310m, 570m, 1.1B.
                        )
        self.clf = clf
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
                