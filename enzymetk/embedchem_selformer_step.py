from enzymetk.step import Step
import pandas as pd
from tempfile import TemporaryDirectory
import subprocess
from pathlib import Path
import logging
import datetime


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SelFormer(Step):
    
    def __init__(self, value_col: str, id_col: str, selformer_dir: str, model_file: str):
        self.value_col = value_col
        self.id_col = id_col
        self.selformer_dir = selformer_dir
        self.model_file = model_file

    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        sub_df = df[[self.id_col, self.value_col]]
        # Have to change it so that selformer can run
        sub_df.columns = ['chembl_id', 'canonical_smiles']
        with TemporaryDirectory() as tmp_dir:
            now = datetime.datetime.now()
            formatted_date = now.strftime("%Y%m%d%H%M%S")
            label = f'selformer_{formatted_date}'
            output_filename = f'{tmp_dir}/{label}.csv'
            input_filename = f'{tmp_dir}/{label}.tsv'
            sub_df.to_csv(input_filename, sep='\t', index=False)
            cmd = ['python', Path(__file__).parent/'selformer_run.py', '--out', output_filename, 
                                     '--input', input_filename, '--label', label, '--dir', self.selformer_dir, 
                                     '--model', self.model_file]
            self.run(cmd)
            df = pd.read_csv(output_filename)
     
        return df
