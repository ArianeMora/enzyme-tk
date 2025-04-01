from enzymetk.step import Step
import pandas as pd
import numpy as np
from multiprocessing.dummy import Pool as ThreadPool
from tempfile import TemporaryDirectory
import os
import subprocess


class ProteInfer(Step):
    
    def __init__(self, id_col: str, seq_col: str, proteinfer_dir: str, num_threads: int = 1, 
                 ec1_filter: list = None, ec2_filter: list = None, ec3_filter: list = None, ec4_filter: list = None, 
                 env_name: str = 'proteinfer', args: list = None):
        """Initialize the CLEAN step for enzyme classification.
        
        Filters are lists of strings which are the EC values to keep. If None then keep all EC values.
        
        Parameters
        ----------
        id_col : str
            Name of the column containing sequence identifiers in the input DataFrame
        seq_col : str
            Name of the column containing protein sequences in the input DataFrame
        clean_dir : str
            Path to the CLEAN software directory containing the CLEAN_infer_fasta.py script
        num_threads : int, optional
            Number of parallel threads to use for processing (default=1)
        ec1_filter : list, optional
            List of EC1 values to filter by (default=None) if None then keep all EC1 values also use '-' to keep missing values
        ec2_filter : list, optional
            List of EC2 values to filter by (default=None) if None then keep all EC2 values also use '-' to keep missing values 
        ec3_filter : list, optional
            List of EC3 values to filter by (default=None) if None then keep all EC3 values also use '-' to keep missing values e.g. ['3', '-']
        ec4_filter : list, optional
            List of EC4 values to filter by (default=None) if None then keep all EC4 values also use '-' to keep missing values e.g. ['1', '-']
            
        Notes
        -----
        CLEAN requires a GPU and the 'clean' conda environment to be installed.
        The CLEAN software directory should contain the following structure:
        - data/inputs/ : Directory for temporary fasta files
        - results/inputs/ : Directory where CLEAN outputs results
        """
        self.env_name = env_name
        self.args = args
        self.id_col = id_col
        self.proteinfer_dir = proteinfer_dir
        self.seq_col = seq_col # This is the column which has the sequence in it 
        self.num_threads = num_threads
        self.ec1_filter = ec1_filter
        self.ec2_filter = ec2_filter
        self.ec3_filter = ec3_filter
        self.ec4_filter = ec4_filter
        
    def __execute(self, data: list) -> np.array:
        df, tmp_dir = data
        # Make sure in the directory of proteinfer
        # Create the fasta file based on the id and the sequence value columns
        input_filename = f'{tmp_dir}proteinfer.fasta'
        output_filename = f'{tmp_dir}proteinfer.txt'
        
        # write fasta file which is the input for proteinfer
        with open(input_filename, 'w+') as fout:
            for entry, seq in df[[self.id_col, self.seq_col]].values:
                fout.write(f'>{entry.strip()}\n{seq.strip()}\n')
        
        os.chdir(self.proteinfer_dir)
        cmd = ['conda', 'run', '-n', self.env_name, 'python3', 
                os.path.join(self.proteinfer_dir, f'proteinfer.py'),
                '-i', input_filename,
                '-o', output_filename]
        if self.args is not None:
            # Add the args to the command
            cmd.extend(self.args)
        self.run(cmd)
        df = pd.read_csv(output_filename, sep='\t')
        
        # Change back to the current folder     
        dir_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(dir_path)
        
        return df
    
    def __clean_df(self, results: pd.DataFrame) -> pd.DataFrame:
        """ 
        Clean the proteinfer formatted file
        """ 
        results['predicted_ecs'] = [ec.split(':')[1] if 'EC:' in ec else 'None' for ec in results['predicted_label'].values]
        # Remobe missing ECs
        results = results[results['predicted_ecs'] != 'None']
        
        # ------------- Separate out ECs ------------------
        results['EC1'] = [r.split('.')[0] for r in results['predicted_ecs'].values]
        results['EC2'] = [r.split('.')[1] for r in results['predicted_ecs'].values]
        results['EC3'] = [r.split('.')[2] for r in results['predicted_ecs'].values]
        results['EC4'] = [r.split('.')[3] for r in results['predicted_ecs'].values]
        # Filter to only have one EC per seqeunce 
        # ------------- Group ------------------
        # Now we want to group by the sequence_name and keep only the highest confidence level assignment
        df = results.groupby('sequence_name')
        rows = []
        for grp in df:
            top_row = grp[1].sort_values(by='predicted_label', ascending=False).values[0]
            rows.append(top_row)
        df = pd.DataFrame(rows, columns=results.columns)
                
        # ------------- Filter to EC XXXX ------------------
        if self.ec1_filter is not None:
            df = df[df['EC1'].isin(self.ec1_filter)]
        if self.ec2_filter is not None:
            df = df[df['EC2'].isin(self.ec2_filter)]
        if self.ec3_filter is not None:
            df = df[df['EC3'].isin(self.ec3_filter)]
        if self.ec4_filter is not None:
            df = df[df['EC4'].isin(self.ec4_filter)]
        return df
        
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        with TemporaryDirectory() as tmp_dir:
            if self.num_threads > 1:
                data = []
                df_list = np.array_split(df, self.num_threads)
                pool = ThreadPool(self.num_threads)
                for df_chunk in df_list:
                    data.append([df_chunk, tmp_dir])
                results = pool.map(self.__execute, data)
                df = pd.DataFrame()
                for dfs in results:
                    df = pd.concat([df, dfs])
                #df = self.__clean_df(df)
                return df
            else:
                df = self.__execute([df, tmp_dir])
                #df = self.__clean_df(df)
                return df