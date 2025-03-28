# #os.system('python run.py --seed 111 --pdb_path "./test_outputs/QHH_0.pdb" --fixed_residues "A19 A20 A21 A59 A60 A61 A90 A91 A92" --checkpoint_path_sc "./model_params/ligandmpnn_sc_v_32_002_16.pt" --out_folder "./outputs/QHH"')
#os.system('python run.py --seed 111 --pdb_path "./test_outputs/QHH_0.pdb" --fixed_residues "A19 A20 A21 A59 A60 A61 A90 A91 A92" --checkpoint_path_sc "./model_params/ligandmpnn_sc_v_32_002_16.pt" --out_folder "./outputs/QHH"')
"""
Install clean and then you need to activate the environment and install and run via that. 

Honestly it's a bit hacky the way they do it, not bothered to change things so have to save the data to their
repo and then copy it out of it.
"""
from enzymetk.step import Step
import pandas as pd
import numpy as np
from tempfile import TemporaryDirectory
import subprocess
import logging
import os

class LigandMPNN(Step):
    
    def __init__(self, pdb_column_name: str, ligand_mpnn_dir: str, output_dir: str, tmp_dir: str = None, args=None, num_threads: int = 1, env_name: str = 'ligandmpnn_env'):
        self.pdb_column_name = pdb_column_name
        self.ligand_mpnn_dir = ligand_mpnn_dir
        self.output_dir = output_dir
        self.tmp_dir = tmp_dir
        self.args = args
        self.num_threads = num_threads
        self.env_name = env_name
        self.logger = logging.getLogger(__name__)
        
    def __execute(self, data: list) -> np.array:
        df, tmp_dir = data
        # Get the PDB files from the column
        output_filenames = []
        # You have to change the directory to the ligandmpnn directory
        os.chdir(self.ligand_mpnn_dir)
        
        for pdb_file in df[ self.pdb_column_name].values:
            cmd = ['conda', 'run', '-n', self.env_name, 'python3', f'{self.ligand_mpnn_dir}run.py', '--pdb_path', pdb_file,  '--out_folder', f'{self.output_dir}']
            if self.args is not None:
                cmd.extend(self.args)
            result = subprocess.run(cmd, check=True)
            if result.stderr:
                self.logger.error(result.stderr)
            else:
                output_filenames.append(f'{self.output_dir}{pdb_file.split("/")[-1].split(".")[0]}')
            self.logger.info(result.stdout)
        df['inpainted_pdb'] = output_filenames
        return df
    
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.tmp_dir is not None:
            return self.__execute([df, self.tmp_dir])
        with TemporaryDirectory() as tmp_dir:
            if self.num_threads > 1:
                output_filenames = []
                df_list = np.array_split(df, self.num_threads)
                for df_chunk in df_list:
                    output_filenames.append(self.__execute(df_chunk, tmp_dir))
                    
                df = pd.DataFrame()
                for tmp_df in output_filenames:
                    df = pd.concat([df, tmp_df])
                return df
    
            return self.__execute([df, tmp_dir])
            return df