from rxnfp.transformer_fingerprints import RXNBERTFingerprintGenerator, get_default_model_and_tokenizer
import pandas as pd
import pickle
import argparse


def run_rxnfp(output_filename, input_filename, label):
    df = pd.read_csv(input_filename)
    rxns = df[label].values
    model, tokenizer = get_default_model_and_tokenizer()
    rxnfp_generator = RXNBERTFingerprintGenerator(model, tokenizer)
    fps = rxnfp_generator.convert_batch(rxns)
    df['rxnfp'] = fps
    with open(output_filename, 'wb') as file:
        pickle.dump(df, file)
        
def parse_args():
    parser = argparse.ArgumentParser(description="Run rxnfp on a dataset")
    parser.add_argument('-out', '--out', required=True, help='Path to the output directory')
    parser.add_argument('-input', '--input', type=str, required=True, help='path to the dataframe')
    parser.add_argument('-label', '--label', type=str, required=True, help='label of the column')
    return parser.parse_args()

def main():
    args = parse_args()
    run_rxnfp(args.out, args.input, args.label)

main()