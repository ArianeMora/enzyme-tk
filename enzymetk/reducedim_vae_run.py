import pickle
import argparse
import pandas as pd
import numpy as np
from scivae import VAE
import json

def run_vae(output_dir, input_filename, value_column, method, config_file, label, id_column):
    
    # Load the input dataset
    with open(input_filename, 'rb') as file:
            chem_df = pickle.load(file)

    chem_encodings = np.asarray([np.asarray(x) for x in chem_df[value_column].values])
    
    # Load in the config
    with open(config_file, 'r') as f:
        config = json.load(f)
        
    # Add some defaults
    if config.get('batch_size') is None:
        config['batch_size'] = 100
    if config.get('epochs') is None:
        config['epochs'] = 100
    if config.get('early_stop') is None:
        config['early_stop'] = True
    vae_mse = VAE(chem_encodings, chem_encodings, np.ones(len(chem_encodings)), config, 'esm_label')
    # Set batch size and number of epochs
    if method == 'train':
        vae_mse.encode('default', epochs=config['epochs'], batch_size=config['batch_size'], early_stop=config['early_stop'])
        # Save this
        vae_mse.save(weight_file_path=f'{output_dir}{label}_model_weights.h5', optimizer_file_path=f'{output_dir}{label}_model_optimiser.json',
                config_json=f'{output_dir}{label}_config.json')
    elif method == 'encode':
        # load this
        vae_mse.load(weight_file_path=f'{output_dir}{label}_model_weights.h5', optimizer_file_path=f'{output_dir}{label}_model_optimiser.json',
                config_json=f'{output_dir}{label}_config.json')
            
    encoded_data_vae_mse = vae_mse.encode_new_data(chem_encodings)
    
    df = pd.DataFrame()
    df['id'] = chem_df[f'{id_column}'].values
    df['encoding'] = [x for x in encoded_data_vae_mse]

    # Save the encoded data
    with open(f'{output_dir}{label}.pkl', 'wb') as file:
        pickle.dump(df, file)
        
def parse_args():
    parser = argparse.ArgumentParser(description="Run VAE dimensionality reduction on a dataset")
    parser.add_argument('-o', '--out', required=True, help='Path to the output directory')
    parser.add_argument('-i', '--input', type=str, required=True, help='path to the dataframe')
    parser.add_argument('-v', '--value', type=str, required=True, help='label of the column which has the values for encoding')
    parser.add_argument('-m', '--method', type=str, required=True, help='either to encode or train a VAE')
    parser.add_argument('-c', '--config', type=str, required=True, help='config file path as JSON')
    parser.add_argument('-l', '--label', type=str, required=True, help='run label for saving')
    parser.add_argument('-d', '--id', type=str, required=True, help='id column')

    return parser.parse_args()

def main():
    args = parse_args()
    # def run_vae(output_filename, input_filename, value_column, method, config_file, label_column, id_column):
    run_vae(args.out, args.input, args.value, args.method, args.config, args.label, args.id)


main()
