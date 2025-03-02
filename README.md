# A pipeline for enzyme engineering

## Installation

```bash
source enzymetk/conda_envs/install_all.sh
```

## Usage

If you have any issues at all just email me using my caltech email: `amora at caltech . edu`

## Things to note

All the tools use the conda env of `enzymetk` by default.

If you want to use a different conda env, you can do so by passing the `env_name` argument to the constructor of the step.

For example:

```python
proteinfer = ProteInfer(env_name='proteinfer')
```

## Arguments

All the arguments are passed to the constructor of the step, the ones that are required are passed as arguments to the constructor and the ones that are optional are passed as a list to the `args` argument, this needs to be a list as one would normally pass arguments to a command line tool.

For example:

```python
proteinfer = ProteInfer(env_name='proteinfer', args=['--num_threads', '10'])
```
For those wanting to use specific arguments, check the individual tools for specifics. 

## Steps

The steps are the main building blocks of the pipeline. They are responsible for executing the individual tools.

### BLAST

BLAST is a tool for searching a database of sequences for similar sequences. Here you can either pass a database that you have already created or pass the sequences as part of your dataframe and pass the label column (this needs to have two values: reference and query) reference refers to sequences that you want to search against and query refers to sequences that you want to search for.

```python
id_col = 'Entry'
seq_col = 'Sequence'
label_col = 'label'
rows = [['AXE2_TALPU', 'query', 'MHSKFFAASLLGLGAAAIPLEGVMEKRSCPAIHVFGARETTASPGYGSSSTVVNGVLSAYPGSTAEAINYPACGGQSSCGGASYSSSVAQGIAAVASAVNSFNSQCPSTKIVLVGYSQGGEIMDVALCGGGDPNQGYTNTAVQLSSSAVNMVKAAIFMGDPMFRAGLSYEVGTCAAGGFDQRPAGFSCPSAAKIKSYCDASDPYCCNGSNAATHQGYGSEYGSQALAFVKSKLG'],
        ['AXE2_TALPU', 'reference', 'MHSKFFAASLLGLGAAAIPLEGVMEKRSCPAIHVFGARETTASPGYGSSSTVVNGVLSAYPGSTAEAINYPACGGQSSCGGASYSSSVAQGIAAVASAVNSFNSQCPSTKIVLVGYSQGGEIMDVALCGGGDPNQGYTNTAVQLSSSAVNMVKAAIFMGDPMFRAGLSYEVGTCAAGGFDQRPAGFSCPSAAKIKSYCDASDPYCCNGSNAATHQGYGSEYGSQALAFVKSKLG'],
        ['AXE2_GEOSE', 'reference', 'MKIGSGEKLLFIGDSITDCGRARPEGEGSFGALGTGYVAYVVGLLQAVYPELGIRVVNKGISGNTVRDLKARWEEDVIAQKPDWVSIMIGINDVWRQYDLPFMKEKHVYLDEYEATLRSLVLETKPLVKGIILMTPFYIEGNEQDPMRRTMDQYGRVVKQIAEETNSLFVDTQAAFNEVLKTLYPAALAWDRVHPSVAGHMILARAFLREIGFEWVRSR'], 
        ['AXE7A_XYLR2', 'referece', 'MFNFAPKQTTEMKKLLFTLVFVLGSMATALAENYPYRADYLWLTVPNHADWLYKTGERAKVEVSFCLYGMPQNVEVAYEIGPDMMPATSSGKVTLKNGRAVIDMGTMKKPGFLDMRLSVDGKYQHHVKVGFSPELLKPYTKNPQDFDAFWKANLDEARKTPVSVSCNKVDKYTTDAFDCYLLKIKTDRRHSIYGYLTKPKKAGKYPVVLCPPGAGIKTIKEPMRSTFYAKNGFIRLEMEIHGLNPEMTDEQFKEITTAFDYENGYLTNGLDDRDNYYMKHVYVACVRAIDYLTSLPDWDGKNVFVQGGSQGGALSLVTAGLDPRVTACVANHPALSDMAGYLDNRAGGYPHFNRLKNMFTPEKVNTMAYYDVVNFARRITCPVYITWGYNDNVCPPTTSYIVWNLITAPKESLITPINEHWTTSETNYTQMLWLKKQVK'], 
        ['A0A0B8RHP0_LISMN', 'reference', 'MKKLLFLGDSVTDAGRDFENDRELGHGYVKIIADQLEQEDVTVINRGVSANRVADLHRRIEADAISLQPDVVTIMIGINDTWFSFSRWEDTSVTAFKEVYRVILNRIKTETNAELILMEPFVLPYPEDRKEWRGDLDPKIGAVRELAAEFGATLIPLDGLMNALAIKHGPTFLAEDGVHPTKAGHEAIASTWLEFTK']]
df = pd.DataFrame(rows, columns=[id_col, label_col, seq_col])
df << (BLAST(id_col, seq_col, label_col) >> Save('tmp/blast_test.pkl'))
```

### ActiveSitePred

ActiveSitePred is a tool for predicting the active site of an enzyme. This returns a dataframe with the active site prediction for each sequence, and the probability of the active site. Note we use a zero index for the active site prediction while UniProt uses a one index.

```python
squidly_dir = '/disk1/share/software/AS_inference/' # This should be where you downloaded the data from zotero, there is a folder in there called AS_inference
num_threads = 1
id_col = 'Entry'
seq_col = 'Sequence'
rows = [['AXE2', 'MKIGSGEKLLFIGDSITDCGRARPEGEGSFGALGTGYVAYVVGLLQAVYPELGIRVVNKGISGNTVRDLKARWEEDVIAQKPDWVSIMIGINDVWRQYDLPFMKEKHVYLDEYEATLRSLVLETKPLVKGIILMTPFYIEGNEQDPMRRTMDQYGRVVKQIAEETNSLFVDTQAAFNEVLKTLYPAALAWDRVHPSVAGHMILARAFLREIGFEWVRSR'], 
        ['H7C0D0', 'XRAHREIKDIFYKAIQKRRQSQEKIDDILQTLLDATYKDGRPLTDDEVAGMLIGLLLAGQHTSSTTSAWMGFFLARDKTLQKKCYLEQKTVCGENLPPLTYDQLKDLNLLDRCIKETLRLRPPIMIMMRMARTPQTVAGYTIPPGHQDNPASGEKFAYVPFGAGRHRCIGENFAYVQIKTIWSTMLRLYEFDLIDGYFPTVNYTTMIHTPENPVIRYKRRSK']]
df = pd.DataFrame(rows, columns=[id_col, seq_col])
print(df)
df << (ActiveSitePred(id_col, seq_col, squidly_dir, num_threads) >> Save('tmp/squidly_as_pred.pkl'))

```

### Chai

Chai is a tool for predicting the structure of a protein and a ligand, this tool outputs the data to a new folder and creates directories based on the id that is passed. We return the paths to the specific structure for each id in the returned dataframe.

Requres the `docko` conda environment to be created.

```python
output_dir = 'tmp/'
num_threads = 1
id_col = 'Entry'
seq_col = 'Sequence'
substrate_col = 'Substrate'
rows = [['P0DP23', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC'], 
        ['AXE2', 'MKIGSGEKLLFIGDSITDCGRARPEGEGSFGALGTGYVAYVVGLLQAVYPELGIRVVNKGISGNTVRDLKARWEEDVIAQKPDWVSIMIGINDVWRQYDLPFMKEKHVYLDEYEATLRSLVLETKPLVKGIILMTPFYIEGNEQDPMRRTMDQYGRVVKQIAEETNSLFVDTQAAFNEVLKTLYPAALAWDRVHPSVAGHMILARAFLREIGFEWVRSR', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC']]
df = pd.DataFrame(rows, columns=[id_col, seq_col, substrate_col])
print(df)
df << (Chai(id_col, seq_col, substrate_col, f'{output_dir}', num_threads) >> Save(f'{output_dir}test.pkl'))

```

### ChemBERTa

ChemBERTa2 encodes reactions and SMILES strings into a vector space. Note this requires the base environment, i.e. `enzymetk` conda env.

```python
from steps.embedchem_chemberta_step import ChemBERT
from steps.save_step import Save

output_dir = 'tmp/'
num_threads = 1
id_col = 'Entry'
seq_col = 'Sequence'
substrate_col = 'Substrate'
rows = [['P0DP23', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC'], 
        ['P0DP24', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC']]
df = pd.DataFrame(rows, columns=[id_col, seq_col, substrate_col])
df << (ChemBERT(id_col, substrate_col, num_threads) >> Save(f'{output_dir}chemberta.pkl'))
```

### CLEAN

CLEAN is a tool for predicting the EC number of an enzyme.

```python

output_dir = 'tmp/'
num_threads = 1
id_col = 'Entry'
seq_col = 'Sequence'
substrate_col = 'Substrate'
rows = [['P0DP23', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC'], 
        ['AXE2', 'MKIGSGEKLLFIGDSITDCGRARPEGEGSFGALGTGYVAYVVGLLQAVYPELGIRVVNKGISGNTVRDLKARWEEDVIAQKPDWVSIMIGINDVWRQYDLPFMKEKHVYLDEYEATLRSLVLETKPLVKGIILMTPFYIEGNEQDPMRRTMDQYGRVVKQIAEETNSLFVDTQAAFNEVLKTLYPAALAWDRVHPSVAGHMILARAFLREIGFEWVRSR', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC']]
df = pd.DataFrame(rows, columns=[id_col, seq_col, substrate_col])
# This should be relative to the location of the script if you installed via the install_all.sh script
# Note you need to have downloaded their predictive models (ToDo )
clean_dir = 'software/CLEAN/app/'
df << (CLEAN(id_col, seq_col, clean_dir, num_threads=num_threads) >> Save(f'clean_missing_EC_seqs.pkl'))


```
### ClustalOmega

ClustalOmega is a tool for aligning a set of sequences. This gets installed to the system (expecting a linux machine) and added to the bash path.

```python
from steps.generate_msa_step import ClustalOmega
from steps.save_step import Save
import pandas as pd

id_col = 'Entry'
seq_col = 'Sequence'
label_col = 'label'
rows = [['AXE2_TALPU', 'query', 'MHSKFFAASLLGLGAAAIPLEGVMEKRSCPAIHVFGARETTASPGYGSSSTVVNGVLSAYPGSTAEAINYPACGGQSSCGGASYSSSVAQGIAAVASAVNSFNSQCPSTKIVLVGYSQGGEIMDVALCGGGDPNQGYTNTAVQLSSSAVNMVKAAIFMGDPMFRAGLSYEVGTCAAGGFDQRPAGFSCPSAAKIKSYCDASDPYCCNGSNAATHQGYGSEYGSQALAFVKSKLG'],
        ['AXE2_TALPU', 'reference', 'MHSKFFAASLLGLGAAAIPLEGVMEKRSCPAIHVFGARETTASPGYGSSSTVVNGVLSAYPGSTAEAINYPACGGQSSCGGASYSSSVAQGIAAVASAVNSFNSQCPSTKIVLVGYSQGGEIMDVALCGGGDPNQGYTNTAVQLSSSAVNMVKAAIFMGDPMFRAGLSYEVGTCAAGGFDQRPAGFSCPSAAKIKSYCDASDPYCCNGSNAATHQGYGSEYGSQALAFVKSKLG'],
        ['AXE2_GEOSE', 'reference', 'MKIGSGEKLLFIGDSITDCGRARPEGEGSFGALGTGYVAYVVGLLQAVYPELGIRVVNKGISGNTVRDLKARWEEDVIAQKPDWVSIMIGINDVWRQYDLPFMKEKHVYLDEYEATLRSLVLETKPLVKGIILMTPFYIEGNEQDPMRRTMDQYGRVVKQIAEETNSLFVDTQAAFNEVLKTLYPAALAWDRVHPSVAGHMILARAFLREIGFEWVRSR'], 
        ['AXE7A_XYLR2', 'referece', 'MFNFAPKQTTEMKKLLFTLVFVLGSMATALAENYPYRADYLWLTVPNHADWLYKTGERAKVEVSFCLYGMPQNVEVAYEIGPDMMPATSSGKVTLKNGRAVIDMGTMKKPGFLDMRLSVDGKYQHHVKVGFSPELLKPYTKNPQDFDAFWKANLDEARKTPVSVSCNKVDKYTTDAFDCYLLKIKTDRRHSIYGYLTKPKKAGKYPVVLCPPGAGIKTIKEPMRSTFYAKNGFIRLEMEIHGLNPEMTDEQFKEITTAFDYENGYLTNGLDDRDNYYMKHVYVACVRAIDYLTSLPDWDGKNVFVQGGSQGGALSLVTAGLDPRVTACVANHPALSDMAGYLDNRAGGYPHFNRLKNMFTPEKVNTMAYYDVVNFARRITCPVYITWGYNDNVCPPTTSYIVWNLITAPKESLITPINEHWTTSETNYTQMLWLKKQVK'], 
        ['A0A0B8RHP0_LISMN', 'reference', 'MKKLLFLGDSVTDAGRDFENDRELGHGYVKIIADQLEQEDVTVINRGVSANRVADLHRRIEADAISLQPDVVTIMIGINDTWFSFSRWEDTSVTAFKEVYRVILNRIKTETNAELILMEPFVLPYPEDRKEWRGDLDPKIGAVRELAAEFGATLIPLDGLMNALAIKHGPTFLAEDGVHPTKAGHEAIASTWLEFTK']]
df = pd.DataFrame(rows, columns=[id_col, label_col, seq_col])
df << (ClustalOmega(id_col, seq_col) >> Save('tmp/clustalomega_test.pkl'))
```

### CREEP

CREEP is a tool for predicting the EC number of a reaction. At the moment it only supports reactions to EC however we are extending this to other modalities. 

```python
from steps.annotateEC_CREEP_step import CREEP
from steps.save_step import Save
import pandas as pd

# CREEP expects you to have downloaded the data from the zotero page and put it in the data/CREEP folder
output_dir = 'tmp/'
df = pd.DataFrame({'EC number': ['1.1.1.1', '1.1.1.2'], 
                   'Sequence': ['MALWMRLLPLLALLALWGPDPAAA', 'MALWMRLLPLLALLALWGPDPAAA'], 
                   'Reaction': ['O=P(OC1=CC=CC=C1)(OC2=CC=CC=C2)OC3=CC=CC=C3>>O=P(O)(OC4=CC=CC=C4)OC5=CC=CC=C5.OC6=CC=CC=C6',
                                'O=P(OC1=CC=CC=C1)(OC2=CC=CC=C2)OC3=CC=CC=C3>>O=P(O)(OC4=CC=CC=C4)OC5=CC=CC=C5.OC6=CC=CC=C6']})
id_col = 'Entry'
reaction_col = 'Reaction'

df << (CREEP(id_col, reaction_col, CREEP_cache_dir='/disk1/share/software/CREEP/data/', CREEP_dir='/disk1/share/software/CREEP/',
            modality='reaction', reference_modality='protein') >> Save(f'{output_dir}CREEP_test_protein.pkl'))
```

### EmbedESM

EmbedESM is a tool for embedding a set of sequences using ESM2.

```python
from steps.embedprotein_esm_step import EmbedESM
from steps.save_step import Save
import pandas as pd

id_col = 'Entry'
seq_col = 'Sequence'
label_col = 'ActiveSite'
rows = [['AXE2_TALPU', '10', 'MHSKFFAASLLGLGAAAIPLEGVMEKRSCPAIHVFGARETTASPGYGSSSTVVNGVLSAYPGSTAEAINYPACGGQSSCGGASYSSSVAQGIAAVASAVNSFNSQCPSTKIVLVGYSQGGEIMDVALCGGGDPNQGYTNTAVQLSSSAVNMVKAAIFMGDPMFRAGLSYEVGTCAAGGFDQRPAGFSCPSAAKIKSYCDASDPYCCNGSNAATHQGYGSEYGSQALAFVKSKLG'],
        ['AXE2_GEOSE', '1|2', 'MKIGSGEKLLFIGDSITDCGRARPEGEGSFGALGTGYVAYVVGLLQAVYPELGIRVVNKGISGNTVRDLKARWEEDVIAQKPDWVSIMIGINDVWRQYDLPFMKEKHVYLDEYEATLRSLVLETKPLVKGIILMTPFYIEGNEQDPMRRTMDQYGRVVKQIAEETNSLFVDTQAAFNEVLKTLYPAALAWDRVHPSVAGHMILARAFLREIGFEWVRSR'], 
        ['AXE7A_XYLR2', '1', 'MFNFAPKQTTEMKKLLFTLVFVLGSMATALAENYPYRADYLWLTVPNHADWLYKTGERAKVEVSFCLYGMPQNVEVAYEIGPDMMPATSSGKVTLKNGRAVIDMGTMKKPGFLDMRLSVDGKYQHHVKVGFSPELLKPYTKNPQDFDAFWKANLDEARKTPVSVSCNKVDKYTTDAFDCYLLKIKTDRRHSIYGYLTKPKKAGKYPVVLCPPGAGIKTIKEPMRSTFYAKNGFIRLEMEIHGLNPEMTDEQFKEITTAFDYENGYLTNGLDDRDNYYMKHVYVACVRAIDYLTSLPDWDGKNVFVQGGSQGGALSLVTAGLDPRVTACVANHPALSDMAGYLDNRAGGYPHFNRLKNMFTPEKVNTMAYYDVVNFARRITCPVYITWGYNDNVCPPTTSYIVWNLITAPKESLITPINEHWTTSETNYTQMLWLKKQVK'], 
        ['A0A0B8RHP0_LISMN', '2', 'MKKLLFLGDSVTDAGRDFENDRELGHGYVKIIADQLEQEDVTVINRGVSANRVADLHRRIEADAISLQPDVVTIMIGINDTWFSFSRWEDTSVTAFKEVYRVILNRIKTETNAELILMEPFVLPYPEDRKEWRGDLDPKIGAVRELAAEFGATLIPLDGLMNALAIKHGPTFLAEDGVHPTKAGHEAIASTWLEFTK']]
df = pd.DataFrame(rows, columns=[id_col, label_col, seq_col])
df << (EmbedESM(id_col, seq_col, extraction_method='mean', tmp_dir='tmp/') >> Save('tmp/esm2_test.pkl'))
# You can also extract the active site embedding in addition to the mean embedding
df << (EmbedESM(id_col, seq_col, extraction_method='active_site', active_site_col='ActiveSite', tmp_dir='tmp/') >> Save('tmp/esm2_test_active_site.pkl'))
```

### FoldSeek

See: [FoldSeek](https://github.com/steineggerlab/foldseek)

FoldSeek does a similarity search against a database of structures, it runs in the `enzyme-tk` environment. Similarly to the diamond blast, you can either create databases yourself before hand using the 
foldseek documentation or you can create a database on the fly by passing the dataframe with a column called `label` that has two values: `reference` and `query`.
If you pass a database, you need to pass the path to the database.

The columns expect a path to a pdb file i.e. the output from the `Chai` step.

```python
from steps.similarity_foldseek_step import FoldSeek
from steps.save_step import Save
import pandas as pd

# id_col: str, seq_col: str, proteinfer_dir: str,
output_dir = 'tmp/'
rows = [['tmp/P0DP24/chai/P0DP24_3.cif'],
        ['tmp/P0DP24/chai/P0DP24_1.cif']]
df = pd.DataFrame(rows, columns=['pdbs'])
# foldseek_dir: str, pdb_column_name: str, reference_database: str
pdb_column_name = 'pdbs'
# The foldseek database was created using the folldwing command in this location:
# foldseek databases PDB pdb tmp 
reference_database = '/disk1/share/software/foldseek/structures/pdb/pdb'
df << (FoldSeek(pdb_column_name, reference_database) >> Save(f'{output_dir}pdb_files.pkl'))

```

### LigandMPNN

LigandMPNN is a tool for inpainting the sequence for a protein backbone that has been generated by a generative model.

See: [LigandMPNN](https://github.com/dauparas/LigandMPNN)

```python
from steps.inpaint_ligandMPNN_step import LigandMPNN
from steps.save_step import Save
import pandas as pd

# id_col: str, seq_col: str, proteinfer_dir: str,
# This needs to be the full path to the file since LigandMPNN requires the full path (otherwise it will save to the ligandmpnn directory)
output_dir = '/disk1/ariane/vscode/enzyme-tk/examples/tmp/'
# These have to be the full path to the file since LigandMPNN requires the full path.
rows = [['/disk1/ariane/vscode/enzyme-tk/examples/tmp/P0DP24/chai/P0DP24_3.cif'],
        ['/disk1/ariane/vscode/enzyme-tk/examples/tmp/P0DP24/chai/P0DP24_1.cif']]
df = pd.DataFrame(rows, columns=['pdbs'])
# foldseek_dir: str, pdb_column_name: str, reference_database: str
pdb_column_name = 'pdbs'
ligand_mpnn_dir = '/disk1/share/software/LigandMPNN/'
# See how you need to enclose the fixed residues in quotes make sure any spaces are closed in double quotes!
args = ['--fixed_residues', '"A19 A20 A21 A59 A60 A61 A90 A91 A92"', '--checkpoint_path_sc', f'{ligand_mpnn_dir}model_params/ligandmpnn_sc_v_32_002_16.pt']
df << (LigandMPNN(pdb_column_name, ligand_mpnn_dir, output_dir,args=args) >> Save(f'{output_dir}ligandmpnn_inpainted.pkl'))

```

### Proteinfer

Proteinfer is a tool for predicting the EC number of an enzyme.

```python

output_dir = 'tmp/'
num_threads = 1
id_col = 'Entry'
seq_col = 'Sequence'
substrate_col = 'Substrate'
rows = [['P0DP23', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC'], 
        ['AXE2', 'MKIGSGEKLLFIGDSITDCGRARPEGEGSFGALGTGYVAYVVGLLQAVYPELGIRVVNKGISGNTVRDLKARWEEDVIAQKPDWVSIMIGINDVWRQYDLPFMKEKHVYLDEYEATLRSLVLETKPLVKGIILMTPFYIEGNEQDPMRRTMDQYGRVVKQIAEETNSLFVDTQAAFNEVLKTLYPAALAWDRVHPSVAGHMILARAFLREIGFEWVRSR', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC']]
df = pd.DataFrame(rows, columns=[id_col, seq_col, substrate_col])
# This should be relative to the location of the script if you installed via the install_all.sh script
# Note you need to have downloaded their predictive models (ToDo )
proteinfer_dir = 'software/proteinfer/'
df << (ProteInfer(id_col, seq_col, proteinfer_dir, num_threads=num_threads) >> Save(f'proteinfer.pkl'))
```


### FastTree

FastTree is a tool for constructing a phylogenetic tree.

```python
fasttree = FastTree()
```

### ClustalOmega

ClustalOmega is a tool for aligning a set of sequences.

```python
clustalo = ClustalOmega()
```

### Rxnfp

Rxnfp is a tool for predicting the reaction fingerprint of an enzyme.

```python
rxnfp = Rxnfp()
```

### Metagenomics

Metagenomics is a pipeline for extracting genes and annotating them from metagenomic data.

```python
metagenomics = Metagenomics()
```
