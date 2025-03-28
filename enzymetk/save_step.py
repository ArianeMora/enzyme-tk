from enzymetk.step import Step


import pandas as pd

class Save(Step):
    
    def __init__(self, output_filename: str):
        self.output_filename = output_filename
    
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        df.to_pickle(self.output_filename)
        return df
