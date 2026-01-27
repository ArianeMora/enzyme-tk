from __future__ import annotations
import pandas as pd
from sciutil import SciUtil
import timeit
import logging
import subprocess
import os
import typer
from pathlib import Path
SCRIPT_DIR = Path(__file__).parent.resolve()

u = SciUtil()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
 
def run_script(script_name: str, verbose: bool = True) -> int:
    """Run a shell script from the conda_envs directory."""
    script_path = Path(f'{SCRIPT_DIR}/{script_name}')
    
    if not script_path.exists():
        typer.secho(f"Error: Script {script_name} not found at {script_path}", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    typer.secho(f"Running {script_name}...", fg=typer.colors.BLUE)
    
    try:
        result = subprocess.run(
            ["bash", str(script_path)],
            cwd=str(SCRIPT_DIR),
            check=True,
            capture_output=not verbose,
            text=True,
        )
        typer.secho(f"✓ {script_name} completed successfully", fg=typer.colors.GREEN)
        return 0
    except subprocess.CalledProcessError as e:
        typer.secho(f"✗ {script_name} failed with exit code {e.returncode}", fg=typer.colors.RED)
        if not verbose and e.stderr:
            typer.echo(e.stderr)
        raise typer.Exit(1)
    
class Pipeline():
    
    def __init__(self, *steps: Step):
        self.steps = list(steps)
        
    def __rshift__(self, other: Step) -> Step:
        return Pipeline(*self.steps, other)
                        
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        """ 
        Execute some shit.
        """      
        for step in self.steps:
            df = step.execute(df)
        return df
    
    def __rlshift__(self, other: pd.DataFrame) -> pd.DataFrame:
        return self.execute(other)
        

class Step():
    def __init__(self):
        # Should only have one of these
        self.venv = None
        self.conda = None
        self.exec = "/bin/bash"


    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Execute some shit """ 
        return df
    
    def install_venv(self, env_args=None):
        self.conda = None
        self.venv = None   
        """ Install unimol_tools """   
        cmd = ['uv', 'venv', self.env_name]
        if env_args:
            cmd.extend(env_args)
        self.run(cmd)
        # Ensure pip is up to date and installed
        try:
          cmd = [f'{self.env_name}/bin/python', 'pip', 'install', '--upgrade', 'pip']
          self.run(cmd)
        except:
            try:
                # Need to have this for jupyter envs
                cmd = ['wget', 'https://bootstrap.pypa.io/get-pip.py']
                self.run(cmd)
                cmd = [f'{self.env_name}/bin/python', 'get-pip.py']
                self.run(cmd)
            except:
                print('WARNING, you may not have pip in your virtual env. Manually install.')
                pass
     

    def install_conda(self, env_args=None):
        return
    
    def run(self, cmd: list):
        """ Run a command """   
        result = None
        start = timeit.default_timer()
        # Prioitize running in a venv if we have it
        if self.venv:
            cmd = [self.venv] + cmd
            u.warn_p(['Running in venv:', self.venv])
        elif self.conda:
            cmd = ['conda', 'run', '-n', self.conda] + cmd
        u.dp(['Running command', ' '.join([str(c) for c in cmd])])

        result = subprocess.run(cmd, capture_output=True, 
                                text=True, 
                                check=True)
        
        u.warn_p(['Output:'])
        print(result.stdout)
        if result.stderr:
            u.err_p(['Error:', result.stderr])
            logger.error(result.stderr)
        logger.info(result.stdout)
        u.dp(['Time for command to run (min): ', (timeit.default_timer() - start)/60])
        return result

    def __rshift__(self, other: Step)   :
        return Pipeline(self, other)
        
    def __rlshift__(self, other: pd.DataFrame) -> pd.DataFrame:
        """
        Overriding the right shift operator to allow for the pipeline to be executed.
        """
        return self.execute(other)
    