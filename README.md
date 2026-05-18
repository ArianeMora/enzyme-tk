# A pipeline for enzyme engineering

Enzyme-tk is a collection of tools for enzyme engineering, setup as interoperable modules that act on dataframes. These modules are designed to be imported into pipelines for specific function. For this reason, `steps` as each module is called (e.g. finding similar proteins with `BLAST` would be considered a step) are designed to be as light as possible. An example of a pipeline is the [annotate-e](https://github.com/ArianeMora/annotate-e)  ` pipeline, this acts to annotate a fasta with an ensemble of methods (each is designated as an Enzyme-tk step). 

### Quick Start Colab notebook

If you want to try a colab notebook here is an example: ([colab](https://github.com/ArianeMora/enzyme-tk/blob/main/Enzyme_tk_example.ipynb))

Data link: ```git clone https://huggingface.co/datasets/arianemora/enzyme-tk```

### Moving to a new home: 

Since I started at AITHYRA this is migrating to a new home at [moragroup/enzyme-tk](https://github.com/moragroup/enzyme-tk/wiki/Installations) so will be maintaied there.

### Quick Start Colab notebook

If you want to try a colab notebook here is an example: ([colab](https://github.com/ArianeMora/enzyme-tk/blob/main/Enzyme_tk_example.ipynb))

**If you have any issues installing, let me know - this has been tested only on Linux/Ubuntu. Please post an issue!**

## Installation

## Install base package to import modules

```bash
conda create --name enzymetk python==3.10 -y
# Install torch for your specific cuda version
conda activate enzymetk
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu130
pip install enzymetk==0.0.7
```

### Install only the specific requirements you need (recommended) 

For installation instructions check out the [wiki](https://github.com/moragroup/enzyme-tk/wiki/Installations).


### Install only the specific requirements you need (recomended) 

For this clone the repo and then install the requirements for the specific modules you use 
```bash
git clone git@github.com:ArianeMora/enzyme-tk.git
cd enzymetk/conda_envs/ # would recommend looking at these
# e.g. to install all from within that folder you would do
source install_all.sh
```
For more extensive installation instructions check out the [wiki](https://github.com/moragroup/enzyme-tk/wiki/Installations).
## Usage

If you have any issues at all just email me using my caltech email: `amora at aithyra . ac . at`

This is a work-in progress! e.g. some tools (e.g. proteInfer and CLEAN) require extra data to be downloaded in order to run (like model weights.) I'm working on integrating these atm, buzz me if you need this!

Here are some of the tools that have been implemented to be chained together as a pipeline:

[boltz2](https://github.com/jwohlwend/boltz)
[mmseqs2](https://github.com/soedinglab/mmseqs2)  
[foldseek](https://github.com/steineggerlab/foldseek)  
[diamond](https://github.com/bbuchfink/diamond)  
[proteinfer](https://github.com/google-research/proteinfer)  
[CLEAN](https://github.com/tttianhao/CLEAN)  
[chai](https://github.com/chaidiscovery/chai-lab/)  
[chemBERTa2](https://github.com/seyonechithrananda/bert-loves-chemistry)  
[SELFormer](https://github.com/HUBioDataLab/SELFormer)  
[rxnfp](https://github.com/rxn4chemistry/rxnfp)  
[clustalomega](http://www.clustal.org/omega/)  
[CREEP](https://github.com/jsunn-y/CARE)  
[esm](https://github.com/facebookresearch/esm)  
[LigandMPNN](https://github.com/dauparas/LigandMPNN)  
[vina](https://vina.scripps.edu/)  
[Uni-Mol](https://github.com/deepmodeling/Uni-Mol)  
[fasttree](https://morgannprice.github.io/fasttree/)  
[Porechop](https://github.com/rrwick/Porechop)  
[prokka](https://github.com/tseemann/prokka)  

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

## Syntax

We use the operator `>>` to pass the output of one tool to the next. All expect a dataframe as input, and produce a dataframe as output. You can capture the end by using the `=` sign, or save it.

For example:

```
df = df << (ActiveSitePred(id_col, seq_col, num_threads, tmp_dir='tmp/') >> EmbedESM(id_col, seq_col, extraction_method='mean', 
                     tmp_dir='tmp/', rep_num=36) >> Save('tmp/esm2_test_active_site.pkl'))
```
Will run squidly to predict the active sites first, then pass the sequences to ESM2 then save that new dataframe.

You can chain most steps together, some dataframes remove things like the sequence, when it's not necessary so if you find one that can't be chained but would like to use it as part of a pipeline either let me know or just make a pull request!

## Tools and references
Being a toolkit this is a collection of other tools, which means if you use any of these tools then cite the ones relevant to your work:

[mmseqs2](https://github.com/soedinglab/mmseqs2)  
[foldseek](https://github.com/steineggerlab/foldseek)  
[diamond](https://github.com/bbuchfink/diamond)  
[proteinfer](https://github.com/google-research/proteinfer)  
[CLEAN](https://github.com/tttianhao/CLEAN)  
[chai](https://github.com/chaidiscovery/chai-lab/)  
[chemBERTa2](https://github.com/seyonechithrananda/bert-loves-chemistry)  
[SELFormer](https://github.com/HUBioDataLab/SELFormer)  
[rxnfp](https://github.com/rxn4chemistry/rxnfp)  
[clustalomega](http://www.clustal.org/omega/)  
[CREEP](https://github.com/jsunn-y/CARE)  
[esm](https://github.com/facebookresearch/esm)  
[LigandMPNN](https://github.com/dauparas/LigandMPNN)  
[vina](https://vina.scripps.edu/)  
[Uni-Mol](https://github.com/deepmodeling/Uni-Mol)  
[fasttree](https://morgannprice.github.io/fasttree/)  
[Porechop](https://github.com/rrwick/Porechop)  
[prokka](https://github.com/tseemann/prokka)  


