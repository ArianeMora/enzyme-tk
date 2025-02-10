# Installation instructions

## Enzymetk

I tried to keep it as simple as possible however, this expects to be working off a linux machine.
```bash
./enzymetk/conda_envs/install_all.sh
```

If you get a permission denied you may have to run the following:

```bash
chmod a+x enzymetk/conda_envs/*.sh 
```

If you don't ha ve a GPU you'll need to change the versions for some of the specific tools e.g. RFdiffusion etc.

If any of the specific environments fail to install you can just manually  install each environment yourself, these are in the conda_envs foler.

Note this expects that you download the data file from zenodo which has a copy of the repositories used in this project.