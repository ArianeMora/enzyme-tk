from enzymetk.step import Step
import pandas as pd
from docko.docko import *
import logging
import numpy as np
import os
from multiprocessing.dummy import Pool as ThreadPool

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

    
class Vina(Step):
    
    def __init__(self, id_col: str, structure_col: str, sequence_col: str, 
                 substrate_col: str, substrate_name_col: str, active_site_col: str, output_dir: str, num_threads: int):
        print('Expects active site residues as a string separated by |. Zero indexed.')
        self.id_col = id_col
        self.structure_col = structure_col
        self.sequence_col = sequence_col
        self.substrate_col = substrate_col
        self.substrate_name_col = substrate_name_col
        self.active_site_col = active_site_col  # Expects active site residues as a string separated by |
        self.output_dir = output_dir or None
        self.num_threads = num_threads or 1

    def __execute(self, df: pd.DataFrame) -> pd.DataFrame:
        output_filenames = []
        # ToDo: update to create from sequence if the path doesn't exist.
        for label, structure_path, seq, substrate_smiles, substrate_name, residues in df[[self.id_col, self.structure_col, self.sequence_col, self.substrate_col, self.substrate_name_col, self.active_site_col]].values:
            os.system(f'mkdir {self.output_dir}{label}')
            try:
                residues = str(residues)
                residues = [int(r) + 1 for r in residues.split('|')]
                if not os.path.exists(f'{structure_path}'):
                    # Try get the AF2 structure we expect the label to be the uniprot id
                    get_alphafold_structure(label, f'{self.output_dir}{label}/{label}_AF2.pdb')
                    structure_path = f'{self.output_dir}{label}/{label}_AF2.pdb'
                clean_one_pdb(f'{structure_path}', f'{self.output_dir}{label}/{label}.pdb')
                pdb_to_pdbqt_protein(f'{self.output_dir}{label}/{label}.pdb', f'{self.output_dir}{label}/{label}.pdbqt')
                score = dock(sequence='', protein_name=label, smiles=substrate_smiles, ligand_name=substrate_name, residues=residues, 
                            protein_dir=f'{self.output_dir}', ligand_dir=f'{self.output_dir}', output_dir=f'{self.output_dir}{label}/', pH=7.4,
                            method='vina', size_x=10.0, size_y=10.0, size_z=10.0)
                output_filename = f'{self.output_dir}{label}/{label}.pdb'
                output_filenames.append(output_filename)
            except Exception as e:
                print(f'Error docking {label}: {e}')
                output_filenames.append(None)
        return output_filenames
        
    
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.output_dir:
            if self.num_threads > 1:
                pool = ThreadPool(self.num_threads)
                df_list = np.array_split(df, self.num_threads)
                results = pool.map(self.__execute, df_list)
            else:
                results = self.__execute(df)
            df['output_dir'] = results
            return df
        else:
            print('No output directory provided')