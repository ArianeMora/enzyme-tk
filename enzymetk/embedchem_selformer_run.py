import argparse
import os

def run_selformer(output_filename, input_filename, label, selformer_dir, model_file):
    print(f'Running selformer on {input_filename} with label {label}')
    os.chdir(selformer_dir)
    os.system(f'cp {input_filename} {selformer_dir}data/{label}.txt')
    os.system(f'conda run -n SELFormer_env python3 {selformer_dir}generate_selfies.py --smiles_dataset=data/{label}.txt --selfies_dataset=data/{label}.csv')
    os.system(f'conda run -n SELFormer_env python3 {selformer_dir}produce_embeddings.py --selfies_dataset=data/{label}.csv --model_file={model_file} --embed_file=data/{label}_embedding.csv')
    os.system(f'cp {selformer_dir}data/{label}_embedding.csv {output_filename}')
    os.system(f'rm data/{label}.txt')
    os.system(f'rm data/{label}.csv')
    os.system(f'rm data/{label}_embedding.csv')

def parse_args():
    parser = argparse.ArgumentParser(description="Run selformer on a dataset")
    parser.add_argument('-out', '--out', required=True, help='Path to the output directory')
    parser.add_argument('-input', '--input', type=str, required=True, help='path to the dataframe')
    parser.add_argument('-label', '--label', type=str, required=True, help='label of the column')
    parser.add_argument('-dir', '--dir', type=str, required=True, help='path to the directory')
    parser.add_argument('-model', '--model', type=str, required=True, help='path to the model')
    return parser.parse_args()

def main():
    args = parse_args()
    run_selformer(args.out, args.input, args.label, args.dir, args.model)

main()
