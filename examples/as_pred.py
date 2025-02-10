import sys
sys.path.append('../enzymetk/')
from steps.predict_catalyticsite_step import ActiveSitePred
from steps.save_step import Save
import pandas as pd
import os
os.environ['MKL_THREADING_LAYER'] = 'GNU'

squidly_dir = '/disk1/share/software/AS_inference/'
num_threads = 1
id_col = 'Entry'
seq_col = 'Sequence'
rows = [['P0DP23', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA'], 
        ['P0DP24', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA']]
df = pd.DataFrame(rows, columns=[id_col, seq_col])
print(df)
df << (ActiveSitePred(id_col, seq_col, squidly_dir, num_threads) >> Save('tmp/squidly_as_pred.pkl'))
