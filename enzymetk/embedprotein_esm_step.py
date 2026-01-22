from enzymetk.step import Step
import pandas as pd
from tempfile import TemporaryDirectory
from pathlib import Path
import numpy as np
from tqdm import tqdm 
import os
import torch

    
# First run this: nohup python esm-extract.py esm2_t33_650M_UR50D /disk1/ariane/vscode/degradeo/data/DEHP/uniprot/EC3.1.1_training.fasta /disk1/ariane/vscode/degradeo/data/DEHP/uniprot/encodings --include per_tok & 
def extract_active_site_embedding(df, id_column, residue_columns, encoding_dir, rep_num=33): 
    """ Expects that the entries for the active site df are saved as the filenames in the encoding dir. """
    combined_tensors = []
    mean_tensors = []
    count_fail = 0
    count_success = 0
    for entry, residues in tqdm(df[[id_column, residue_columns]].values):
        try:
            file = Path(encoding_dir + f'/{entry}.pt')
            tensors = []
            if residues is not None and residues != 'None': 
                try:
                    residues = [int(r) for r in residues.split('|')]
                except:
                    residues = []
            else:
                residues = []
            embedding_file = torch.load(file)
            tensor = embedding_file['representations'][rep_num] # have to get the last layer (36) of the embeddings... very dependant on ESM model used! 36 for medium ESM2
            tensors = []
            mean_tensors.append(np.mean(np.asarray(tensor).astype(np.float32), axis=0))
            for residue in residues:
                t = np.asarray(tensor[residue]).astype(np.float32)
                tensors.append(t)
            combined_tensors.append(tensors)
        except Exception as e:
            print(f'Error loading file {file}: {e}')
            count_fail += 1
            mean_tensors.append(None)
            combined_tensors.append(None)
    # HEre is where you do something on the combined tensors
    df['active_embedding'] = combined_tensors
    df['esm_embedding'] = mean_tensors
    print(count_success, count_fail, count_fail + count_success)
    return df

# First run this: nohup python esm-extract.py esm2_t33_650M_UR50D /disk1/ariane/vscode/degradeo/data/DEHP/uniprot/EC3.1.1_training.fasta /disk1/ariane/vscode/degradeo/data/DEHP/uniprot/encodings --include per_tok & 
def extract_mean_embedding(df, id_column, encoding_dir, rep_num=33): 
    """ Expects that the entries for the active site df are saved as the filenames in the encoding dir. """
    tensors = []
    count_fail = 0
    count_success = 0
    for entry in tqdm(df[id_column].values):
        try:
            file = Path(os.path.join(encoding_dir, f'{entry}.pt'))
            embedding_file = torch.load(file)
            tensor = embedding_file['representations'][rep_num] # have to get the last layer (36) of the embeddings... very dependant on ESM model used! 36 for medium ESM2
            t = np.mean(np.asarray(tensor).astype(np.float32), axis=0)
            tensors.append(t)
        except Exception as e:
            print(f'Error loading file {file}: {e}')
            count_fail += 1
            tensors.append(None)

    df['embedding'] = tensors
    print(count_success, count_fail, count_fail + count_success)
    return df

class EmbedESM(Step):
    
    def __init__(self, id_col: str, seq_col: str, model='esm2_t36_3B_UR50D', extraction_method='mean', 
                 active_site_col: str = None, num_threads=1, tmp_dir: str = None, env_name = 'enzymetk', 
                 venv_name = None, 
                 rep_num=-1):
        self.seq_col = seq_col
        self.id_col = id_col
        self.active_site_col = active_site_col
        self.model = model
        self.num_threads = num_threads or 1
        self.extraction_method = extraction_method
        self.tmp_dir = tmp_dir
        self.rep_num = rep_num
        self.conda = env_name
        self.env_name = env_name
        self.venv = venv_name if venv_name else f'{env_name}/bin/python'
        super().__init__()

    def install(self, env_args=None):
        # e.g. env args could by python=='3.1.1.
        self.install_venv(env_args)
        # Now the specific
        try:
            cmd = [f'{self.env_name}/bin/pip', 'install', 'fair-esm']
            self.run(cmd)
        except Exception as e:
            cmd = [f'{self.env_name}/bin/pip3', 'install', 'fair-esm']
            self.run(cmd)
        self.run(cmd)
        # Now set the venv to be the location:
        self.venv = f'{self.env_name}/bin/python'
        print('Finished installing ESM environment. You may need to reactivate your environment now!')
        print(f'Use command: source {self.env_name}/bin/activate')

    def __execute(self, df: pd.DataFrame, tmp_dir: str) -> pd.DataFrame:
        input_filename = f'{tmp_dir}/input.fasta'
        # Check the file doesn't exist in the tmp_dir
        files = os.listdir(tmp_dir)
        done_entries = set([f.split('.')[0] for f in files if f.endswith('.pt')])
        # write fasta file which is the input for proteinfer
        with open(input_filename, 'w+') as fout:
            for entry, seq in df[[self.id_col, self.seq_col]].values:
                if entry not in done_entries:
                    fout.write(f'>{entry.strip()}\n{seq.strip()}\n')
        # Might have an issue if the things are not correctly installed in the same dicrectory 
        self.__run_esm(self.model, input_filename, Path(tmp_dir), repr_layers=[self.rep_num], include_features=['per_tok'], toks_per_batch=4096, truncation_seq_length=1024, nogpu=False)
        if self.extraction_method == 'mean':
            df = extract_mean_embedding(df, self.id_col, tmp_dir, rep_num=self.rep_num)
        elif self.extraction_method == 'active_site':
            if self.active_site_col is None:
                raise ValueError('active_site_col must be provided if extraction_method is active_site')
            df = extract_active_site_embedding(df, self.id_col, self.active_site_col, tmp_dir, rep_num=self.rep_num)
        
        return df
    
    def __run_esm(self, model_location, fasta_file, output_dir, repr_layers=[-1], include_features=[], toks_per_batch=4096, truncation_seq_length=1024, nogpu=False):
        from esm import Alphabet, FastaBatchedDataset, ProteinBertModel, pretrained, MSATransformer
        model, alphabet = pretrained.load_model_and_alphabet(model_location)
        model.eval()
        if isinstance(model, MSATransformer):
            raise ValueError(
                "This script currently does not handle models with MSA input (MSA Transformer)."
            )
        if torch.cuda.is_available() and not nogpu:
            model = model.cuda()
            print("Transferred model to GPU")

        dataset = FastaBatchedDataset.from_file(fasta_file)
        batches = dataset.get_batch_indices(toks_per_batch, extra_toks_per_seq=1)
        data_loader = torch.utils.data.DataLoader(
            dataset, collate_fn=alphabet.get_batch_converter(truncation_seq_length), batch_sampler=batches
        )
        print(f"Read {fasta_file} with {len(dataset)} sequences")

        output_dir.mkdir(parents=True, exist_ok=True)
        return_contacts = "contacts" in include_features

        assert all(-(model.num_layers + 1) <= i <= model.num_layers for i in repr_layers)
        repr_layers = [(i + model.num_layers + 1) % (model.num_layers + 1) for i in repr_layers]

        with torch.no_grad():
            for batch_idx, (labels, strs, toks) in enumerate(data_loader):
                print(
                    f"Processing {batch_idx + 1} of {len(batches)} batches ({toks.size(0)} sequences)"
                )
                if torch.cuda.is_available() and not nogpu:
                    toks = toks.to(device="cuda", non_blocking=True)

                out = model(toks, repr_layers=repr_layers, return_contacts=return_contacts)

                logits = out["logits"].to(device="cpu")
                representations = {
                    layer: t.to(device="cpu") for layer, t in out["representations"].items()
                }
                if return_contacts:
                    contacts = out["contacts"].to(device="cpu")

                for i, label in enumerate(labels):

                    output_file = output_dir / f"{label}.pt"
                    print(output_file)
                    output_file.parent.mkdir(parents=True, exist_ok=True)
                    result = {"label": label}
                    truncate_len = min(truncation_seq_length, len(strs[i]))
                    # Call clone on tensors to ensure tensors are not views into a larger representation
                    # See https://github.com/pytorch/pytorch/issues/1995
                    if "per_tok" in include_features:
                        result["representations"] = {
                            layer: t[i, 1 : truncate_len + 1].clone()
                            for layer, t in representations.items()
                        }
                    if "mean" in include_features:
                        result["mean_representations"] = {
                            layer: t[i, 1 : truncate_len + 1].mean(0).clone()
                            for layer, t in representations.items()
                        }
                    if "bos" in include_features:
                        result["bos_representations"] = {
                            layer: t[i, 0].clone() for layer, t in representations.items()
                        }
                    if return_contacts:
                        result["contacts"] = contacts[i, : truncate_len, : truncate_len].clone()
                    print(result)
                    torch.save(
                        result,
                        output_file,
                    )

    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.tmp_dir is None:
            with TemporaryDirectory() as tmp_dir:
                if self.num_threads > 1:
                    dfs = []
                    df_list = np.array_split(df, self.num_threads)
                    for df_chunk in tqdm(df_list):
                        dfs.append(self.__execute(df_chunk, tmp_dir))
                    df = pd.DataFrame()
                    for tmp_df in tqdm(dfs):
                        df = pd.concat([df, tmp_df])
                    return df
                else:
                    df = self.__execute(df, tmp_dir)
                    return df
        else:
            df = self.__execute(df, self.tmp_dir)
            return df