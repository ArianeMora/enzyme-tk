from enzymetk.generate_msa_step import ClustalOmega
from enzymetk.save_step import Save
import pandas as pd


# output_dir = '/home/helen/degradeo/pipeline/helen_data/'
# input_file = '/home/helen/degradeo/pipeline/helen_data/sequences_test.csv'
# df = pd.read_csv(input_file, sep=';')


# # clustalomega_dir: str, sequence_column_name: str
# clustalomega_dir = '/home/helen/degradeo/software/'
# sequence_column_name = 'sequence'
# df << (ClustalOmega(clustalomega_dir, sequence_column_name) >> Save(f'{output_dir}sequences_aligned.pkl'))