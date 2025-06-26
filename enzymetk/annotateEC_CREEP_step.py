from enzymetk.step import Step
import pandas as pd
from tempfile import TemporaryDirectory
import subprocess
import logging
import numpy as np
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

"""
import os

Example file as input:
Reaction,EC number,Reaction Text,EC3,EC2,EC1
O=C(OCC(CC)CCCC)C1=CC=CC=C1C(OCC(CC)CCCC)=O>>OC(C2=CC=CC=C2C(O)=O)=O,3.1.1.60,DEHP->PA,3.1.1,3.1,3
CCCCC(CC)COC(=O)c1ccccc1C(=O)OCC(CC)CCCC.O>>CCCCC(CC)CO.CCCCC(CC)COC(=O)c1ccccc1C(=O)O,3.1.1.60,DEHP-MEHP,3.1.1,3.1,3

os.system(f'
python step_02_extract_CREEP.py --pretrained_folder=/disk1/share/software/CREEP/data/bioremediation_split --dataset=/disk1/share/software/CREEP/output/DEHP/bioremediation_reaction_test.csv --modality=reaction
')

os.system(f'python downstream_retrieval.py --pretrained_folder=CREEP/$OUTPUT_DIR --query_dataset=$TEST_SET --reference_dataset=all_ECs --query_modality=reaction --reference_modality=protein')
"""
    
class CREEP(Step):
    
    def __init__(self, id_col: str, value_col: str, CREEP_dir: str, CREEP_cache_dir: str, modality: str, reference_modality: str, 
                 env_name: str = 'CREEP', args_extract: list = None, args_retrieval: list = None):
        self.env_name = env_name
        self.id_col = id_col
        self.value_col = value_col  
        self.modality = modality
        self.reference_modality = reference_modality
        self.CREEP_dir = CREEP_dir
        self.CREEP_cache_dir = CREEP_cache_dir
        self.args_extract = args_extract
        self.args_retrieval = args_retrieval
            
    def __execute(self, df: pd.DataFrame, tmp_dir: str):
        tmp_dir = '/disk1/ariane/vscode/degradeo/pipeline/tmp/'
        input_filename = f'{tmp_dir}/creepasjkdkajshdkja.csv'
        df.to_csv(input_filename, index=False)
        cmd = ['conda', 'run', '-n', self.env_name, 'python', f'{self.CREEP_dir}scripts/step_02_extract_CREEP.py', '--pretrained_folder', 
                                 f'{self.CREEP_cache_dir}output/easy_split', 
                                  '--dataset', input_filename,
                                  '--cache_dir', self.CREEP_dir, 
                                  '--modality', self.modality.strip(), 
                                  '--output_dir', f'{tmp_dir}']
        if self.args_extract is not None:
            cmd.extend(self.args_extract)
        result = subprocess.run(cmd, capture_output=True, text=True)
        cmd = ['conda', 'run', '-n', self.env_name, 'python', f'{self.CREEP_dir}scripts/downstream_retrieval.py', '--pretrained_folder',
                                 f'{self.CREEP_cache_dir}output/easy_split', 
                                 '--query_dataset', input_filename, 
                                 '--reference_dataset', 'all_ECs',
                                 '--query_modality', self.modality.strip(),
                                 '--cache_dir', self.CREEP_cache_dir, 
                                 '--output_dir', f'{tmp_dir}',
                                 '--reference_modality', self.reference_modality]
        if self.args_retrieval is not None:
            cmd.extend(self.args_retrieval)
        self.run(cmd)
        output_filename = f'{tmp_dir}/creep_reaction2protein_retrieval_similarities.npy'
        return output_filename
    
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        with TemporaryDirectory() as tmp_dir:
            output_filename = self.__execute(df, tmp_dir)
            df = pd.read_csv(f"{self.CREEP_dir}/data/processed_data/EC_list.txt", header=None)
            data = np.load(output_filename)
            all_ecs = np.load(f"{self.CREEP_dir}/data/output/easy_split/representations/all_ECs_cluster_centers.npy", allow_pickle=True)
            rxn_data = np.load(f"{self.CREEP_dir}/data/output/easy_split/representations/easy_reaction_test_representations.npy", allow_pickle=True)
            data_dict = rxn_data.item()
            print(data_dict)
            data_dict = data_dict['reaction_repr_array']
            data_rxn = all_ecs.item()
            data_rxn = data_rxn['protein_repr_array']
            for i, d in enumerate(data):
                df[f'sim_{i}'] = d
            return df
