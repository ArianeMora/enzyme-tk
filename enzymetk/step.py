from __future__ import annotations
import pandas as pd
from sciutil import SciUtil
import timeit
import logging
import subprocess
import os

u = SciUtil()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
 

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
    
    def install_venv(self):
        return 
    
    def install_conda(self):
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
    