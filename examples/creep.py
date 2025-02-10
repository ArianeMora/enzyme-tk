import sys
sys.path.append('../enzymetk/')

from steps.annotateEC_CREEP_step import CREEP
from steps.save_step import Save
import pandas as pd


df = pd.DataFrame({'EC number': ['1.1.1.1', '1.1.1.2'], 'Sequence': ['MALWMRLLPLLALLALWGPDPAAA', 'MALWMRLLPLLALLALWGPDPAAA']})
id_col = 'Entry'
seq_col = 'Sequence'
df << (CREEP(id_col, seq_col, CREEP_cache_dir='/disk1/share/software/CREEP/data/', CREEP_dir='/disk1/share/software/CREEP/',
            modality='reaction', reference_modality='protein') >> Save('tmp/CREEP_test_protein.pkl'))
