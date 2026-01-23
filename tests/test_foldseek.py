#./foldseek easy-search /home/ariane/degradeo/data/pipeline/p1_predict_activity/p1b_encode_protein/e1_esm/chai/Q0HLQ7/chai/Q0HLQ7_0.cif /home/ariane/degradeo/data/pipeline/p1_predict_activity/p1b_encode_protein/e1_esm/chai/Q0HLQ7/chai/Q0HLQ7_1.cif pdb test_aln.fasta tmp
"""
Install clean and then you need to activate the environment and install and run via that. 

Honestly it's a bit hacky the way they do it, not bothered to change things so have to save the data to their
repo and then copy it out of it.
"""
from enzymetk.step import Step

import logging
import pandas as pd
import numpy as np
from tempfile import TemporaryDirectory
import subprocess
import random
import string
from tqdm import tqdm 

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
from pathlib import Path
import subprocess


PROSTT5_DIR = Path.home() / ".foldseek" / "prostt5"
TMP_DIR = Path.home() / ".foldseek" / "tmp"

PROSTT5_DIR.mkdir(parents=True, exist_ok=True)
TMP_DIR.mkdir(parents=True, exist_ok=True)


class FoldSeek(Step):
    
    def __init__(self, query_column_name: str, reference_database_directory: str, 
                 args=None, num_threads=1, tmp_dir: str = None):
        self.query_column_name = query_column_name # Contains a PBD file path
        self.reference_database_directory = reference_database_directory
        self.tmp_dir = tmp_dir
        self.args = args
        self.num_threads = num_threads
        super().__init__()
        self.venv = None
        self.conda = None

    def make_database(self, df, id_column_name: str, query_column_name: str, database_name: str):
        # Database name is the full path to where you want the database to be
        with open(f'{database_name}seqs.fasta', 'w') as f:
            for i, row in df.iterrows():
                f.write(f'>{row[id_column_name]}\n{row[query_column_name]}\n')

        if not (PROSTT5_DIR / "prostt5-f16.gguf").exists():
            subprocess.run(["foldseek", "databases", "ProstT5", str(PROSTT5_DIR), str(TMP_DIR)], check=True)
        
        subcmd = ["foldseek", "createdb",  f"{database_name}seqs.fasta", database_name, "--prostt5-model", str(PROSTT5_DIR)]

        self.run(subcmd)
                
    def __execute(self, data: list) -> np.array:
        df, tmp_dir = data
        tmp_label = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        # Get the PDB files from the column (each of the queries is a path to a pdb file)
        pdb_files = list(df[self.query_column_name].values)

        cmd = ['foldseek', 'easy-search'] + pdb_files + [f'{self.reference_database_directory}', f'{tmp_dir}{tmp_label}.txt', 'tmp']
        # add in args
        if self.args is not None:
           cmd.extend(self.args)

        self.run(cmd)
        df = pd.read_csv(f'{tmp_dir}{tmp_label}.txt', header=None, sep='\t')
        df.columns = ['query', 'target', 'fident', 'alnlen', 'mismatch', 
                    'gapopen', 'qstart', 'qend', 'tstart', 'tend', 'evalue', 'bits']
        return df
    
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        with TemporaryDirectory() as tmp_dir:
            tmp_dir = self.tmp_dir if self.tmp_dir is not None else tmp_dir
            if self.num_threads > 1:
                output_filenames = []
                df_list = np.array_split(df, self.num_threads)
                for df_chunk in tqdm(df_list):
                    try:
                        output_filenames.append(self.__execute([df_chunk, tmp_dir]))
                    except Exception as e:
                         logger.error(f"Error in executing ESM2 model: {e}")
                         continue
                df = pd.DataFrame()
                print(output_filenames)
                for sub_df in output_filenames:
                    df = pd.concat([df, sub_df])
                return df
            
            else:
                df = self.__execute([df, tmp_dir])
                return df


# id_col: str, seq_col: str, proteinfer_dir: str,
output_dir = 'tmp/'
rows = [['data/example.cif'],
        ['data/example.cif']]
df = pd.DataFrame(rows, columns=['pdbs'])
# foldseek_dir: str, pdb_column_name: str, reference_database: str
pdb_column_name = 'pdbs'
# The foldseek database was created using the folldwing command in this location:
# foldseek databases PDB pdb tmp 
reference_database = '/mnt/labs/data/mora/data/pdb_foldseek/pdb'
fs = FoldSeek(pdb_column_name, reference_database)
df = fs.execute(df)
print(df)
df.to_csv('df.csv')

# Try making a database and then running on that one
id_col = 'Entry'
seq_col = 'Sequence'
label_col = 'ActiveSite'
rows = [['AXE2_TALPU', '10', 'MHSKFFAASLLGLGAAAIPLEGVMEKRSCPAIHVFGARETTASPGYGSSSTVVNGVLSAYPGSTAEAINYPACGGQSSCGGASYSSSVAQGIAAVASAVNSFNSQCPSTKIVLVGYSQGGEIMDVALCGGGDPNQGYTNTAVQLSSSAVNMVKAAIFMGDPMFRAGLSYEVGTCAAGGFDQRPAGFSCPSAAKIKSYCDASDPYCCNGSNAATHQGYGSEYGSQALAFVKSKLG'],
        ['AXE2_GEOSE', '1|2', 'MKIGSGEKLLFIGDSITDCGRARPEGEGSFGALGTGYVAYVVGLLQAVYPELGIRVVNKGISGNTVRDLKARWEEDVIAQKPDWVSIMIGINDVWRQYDLPFMKEKHVYLDEYEATLRSLVLETKPLVKGIILMTPFYIEGNEQDPMRRTMDQYGRVVKQIAEETNSLFVDTQAAFNEVLKTLYPAALAWDRVHPSVAGHMILARAFLREIGFEWVRSR'], 
        ['AXE7A_XYLR2', '1', 'MFNFAPKQTTEMKKLLFTLVFVLGSMATALAENYPYRADYLWLTVPNHADWLYKTGERAKVEVSFCLYGMPQNVEVAYEIGPDMMPATSSGKVTLKNGRAVIDMGTMKKPGFLDMRLSVDGKYQHHVKVGFSPELLKPYTKNPQDFDAFWKANLDEARKTPVSVSCNKVDKYTTDAFDCYLLKIKTDRRHSIYGYLTKPKKAGKYPVVLCPPGAGIKTIKEPMRSTFYAKNGFIRLEMEIHGLNPEMTDEQFKEITTAFDYENGYLTNGLDDRDNYYMKHVYVACVRAIDYLTSLPDWDGKNVFVQGGSQGGALSLVTAGLDPRVTACVANHPALSDMAGYLDNRAGGYPHFNRLKNMFTPEKVNTMAYYDVVNFARRITCPVYITWGYNDNVCPPTTSYIVWNLITAPKESLITPINEHWTTSETNYTQMLWLKKQVK'], 
        ['A0A0B8RHP0_LISMN', '2', 'MKKLLFLGDSVTDAGRDFENDRELGHGYVKIIADQLEQEDVTVINRGVSANRVADLHRRIEADAISLQPDVVTIMIGINDTWFSFSRWEDTSVTAFKEVYRVILNRIKTETNAELILMEPFVLPYPEDRKEWRGDLDPKIGAVRELAAEFGATLIPLDGLMNALAIKHGPTFLAEDGVHPTKAGHEAIASTWLEFTK']]
df = pd.DataFrame(rows, columns=[id_col, label_col, seq_col])
fs.make_database(df, id_col, seq_col, database_name='/mnt/labs/data/mora/code/enzymetk/enzyme-tk/tests/foldseek_folder/db', database_folder='foldseek_folder')

# Now try running the above on this new database
rows = [['data/example.cif'],
        ['data/example.cif']]
df = pd.DataFrame(rows, columns=['pdbs'])
# foldseek_dir: str, pdb_column_name: str, reference_database: str
pdb_column_name = 'pdbs'
# The foldseek database was created using the folldwing command in this location:
# foldseek databases PDB pdb tmp 
fs = FoldSeek(pdb_column_name, '/mnt/labs/data/mora/code/enzymetk/enzyme-tk/tests/foldseek_folder/db')
df = fs.execute(df)
print(df)
df.to_csv('df_v2.csv')