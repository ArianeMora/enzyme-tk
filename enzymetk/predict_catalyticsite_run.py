import argparse
import os


def run_as_inference(output_dir, fasta_file, squidly_dir, toks_per_batch, as_threshold, bs_threshold, cr_model_as, 
                     cr_model_bs, lstm_model_as, lstm_model_bs, esm2_model):
    esm2_model = esm2_model or "esm2_t36_3B_UR50D"
    if esm2_model == "esm2_t36_3B_UR50D":   
        cr_model_as = cr_model_as or f"{squidly_dir}Squidly_CL_3B.pt"
        lstm_model_as = lstm_model_as or f"{squidly_dir}Squidly_LSTM_3B.pth"
    elif esm2_model == "esm2_t48_15B_UR50D":
        cr_model_as = cr_model_as or f"{squidly_dir}Squidly_CL_15B.pt"
        lstm_model_as = lstm_model_as or f"{squidly_dir}Squidly_LSTM_15B.pth"
    as_threshold = 0.97
    #esm2_model = "esm2_t48_15B_UR50D"
    # 	python /scratch/project/squid/code_modular/SQUIDLY_run_model_LSTM.py ${FILE} ${ESM2_MODEL} ${CR_MODEL_AS}
    # ${LSTM_MODEL_AS} ${OUT} --toks_per_batch ${TOKS_PER_BATCH} --AS_threshold ${AS_THRESHOLD} --monitor

    command = f'conda run -n AS_inference python {squidly_dir}SQUIDLY_run_model_LSTM.py \
              {fasta_file} {esm2_model} {cr_model_as} {lstm_model_as} {output_dir} \
              --toks_per_batch {toks_per_batch} --AS_threshold {as_threshold}'
    print(command)
    os.system(command)
    
    
def parse_args():
    parser = argparse.ArgumentParser(description="Run as inference on a dataset")
    parser.add_argument('-out', '--out', required=True, help='Path to the output directory')
    parser.add_argument('-input', '--input', type=str, required=True, help='path to the dataframe')
    parser.add_argument('--squidly_dir', type=str, required=True, help='path to the squidly_dir')
    parser.add_argument('--toks_per_batch', type=int, default=5, help='How many tokens per batch')
    parser.add_argument('--as_threshold', type=float, default=0.90, help='the threshold for active site.')
    parser.add_argument('--bs_threshold', type=float, default=0.85, help='the threshold for binding site.')
    parser.add_argument('--cr_model_as', type=str, help='the path to the active site CR model.')
    parser.add_argument('--cr_model_bs', type=str, help='the path to the binding site CR model.')
    parser.add_argument('--lstm_model_as', type=str, help='the path to the active site LSTM model.')
    parser.add_argument('--lstm_model_bs', type=str, help='the path to the binding site LSTM model.')
    parser.add_argument('--esm2_model', type=str, help='ESM2 model.')
    return parser.parse_args()

def main():
    args = parse_args()
    run_as_inference(args.out, args.input, args.squidly_dir, args.toks_per_batch, args.as_threshold, args.bs_threshold, 
                     args.cr_model_as, args.cr_model_bs, args.lstm_model_as, args.lstm_model_bs, args.esm2_model)

# Removed the if name since we run with subprocess
main()
