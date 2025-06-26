import sys

from enzymetk.annotateEC_CREEP_step import CREEP
from enzymetk.save_step import Save
import pandas as pd

# CREEP expects you to have downloaded the data from the zotero page and put it in the data/CREEP folder
output_dir = 'tmp/'
df = pd.DataFrame({'EC number': ['1.1.1.1', '1.1.1.2'], 
                   'Sequence': ['MALWMRLLPLLALLALWGPDPAAA', 'MALWMRLLPLLALLALWGPDPAAA'], 
                   'Reaction': ['O=P(OC1=CC=CC=C1)(OC2=CC=CC=C2)OC3=CC=CC=C3>>O=P(O)(OC4=CC=CC=C4)OC5=CC=CC=C5.OC6=CC=CC=C6',
                                'O=P(OC1=CC=CC=C1)(OC2=CC=CC=C2)OC3=CC=CC=C3>>O=P(O)(OC4=CC=CC=C4)OC5=CC=CC=C5.OC6=CC=CC=C6']})
id_col = 'Entry'
reaction_col = 'Reaction'

df << (CREEP(id_col, reaction_col, CREEP_cache_dir='/disk4/share/software/CREEP/data/', CREEP_dir='/disk4/share/software/CREEP/',
            modality='reaction', reference_modality='protein') >> Save(f'{output_dir}CREEP_test_protein.pkl'))
