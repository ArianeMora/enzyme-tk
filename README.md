# A pipeline for enzyme engineering

## Installation

```bash
source enzymetk/conda_envs/install_all.sh
```

## Usage


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

## BLAST

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

### Proteinfer

Proteinfer is a tool for predicting the EC number of an enzyme.

```python
proteinfer = ProteInfer()
```

### CLEAN

CLEAN is a tool for predicting the EC number of an enzyme.

```python
clean = CLEAN()
```

### CREEP

CREEP is a tool for predicting the EC number of an enzyme.

```python
creep = CREEP()
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

### LigandMPNN

LigandMPNN is a tool for inpainting the sequence for a protein backbone that has been generated by a generative model.
```python
ligandmpnn = LigandMPNN()
```

### Metagenomics

Metagenomics is a pipeline for extracting genes and annotating them from metagenomic data.

```python
metagenomics = Metagenomics()
```