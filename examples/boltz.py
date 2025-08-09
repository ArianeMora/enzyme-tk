import sys
from enzymetk.dock_boltz_step import Boltz
from enzymetk.save_step import Save
import pandas as pd
import os
os.environ['MKL_THREADING_LAYER'] = 'GNU'

output_dir = 'tmp/boltz/'
num_threads = 1
id_col = 'Entry'
seq_col = 'Sequence'
substrate_col = 'Substrate'
intermediate_col = 'Intermediate'

rows = [['P0DP23_boltz_8999', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC', 'CC1=C(C2=CC3=C(C(=C([N-]3)C=C4C(=C(C(=N4)C=C5C(=C(C(=N5)C=C1[N-]2)C)C=C)C)C=C)C)CCC(=O)[O-])CCC(=O)[O-].[Fe]'], 
       # ['P0DP24_boltz_p1', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC', 'CC1=C(C2=CC3=C(C(=C([N-]3)C=C4C(=C(C(=N4)C=C5C(=C(C(=N5)C=C1[N-]2)C)C=C)C)C=C)C)CCC(=O)[O-])CCC(=O)[O-].[Fe]'],
       # ['P0DP23_boltz_p2', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC', 'CC1=C(C2=CC3=C(C(=C([N-]3)C=C4C(=C(C(=N4)C=C5C(=C(C(=N5)C=C1[N-]2)C)C=C)C)C=C)C)CCC(=O)[O-])CCC(=O)[O-].[Fe]'], 
      #  ['P0DP24_boltz_p3', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC', 'CC1=C(C2=CC3=C(C(=C([N-]3)C=C4C(=C(C(=N4)C=C5C(=C(C(=N5)C=C1[N-]2)C)C=C)C)C=C)C)CCC(=O)[O-])CCC(=O)[O-].[Fe]'],
        ['P0DP24_boltz_p4', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC', 'CC1=C(C2=CC3=C(C(=C([N-]3)C=C4C(=C(C(=N4)C=C5C(=C(C(=N5)C=C1[N-]2)C)C=C)C)C=C)C)CCC(=O)[O-])CCC(=O)[O-].[Fe]']]
df = pd.DataFrame(rows, columns=[id_col, seq_col, substrate_col, intermediate_col])
df = df.head(1)
df << (Boltz(id_col, seq_col, substrate_col, intermediate_col, f'{output_dir}', num_threads) >> Save(f'{output_dir}test.pkl'))

# rows = [['P0DP23_boltz_8888', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC', 'CC1=C(C2=CC3=C(C(=C([N-]3)C=C4C(=C(C(=N4)C=C5C(=C(C(=N5)C=C1[N-]2)C)C=C)C)C=C)C)CCC(=O)[O-])CCC(=O)[O-].[Fe]'], 
#         ['P0DP24_boltz_8888', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC', 'CC1=C(C2=CC3=C(C(=C([N-]3)C=C4C(=C(C(=N4)C=C5C(=C(C(=N5)C=C1[N-]2)C)C=C)C)C=C)C)CCC(=O)[O-])CCC(=O)[O-].[Fe]'],
#         ['P0DP23_boltz_p2', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC', 'CC1=C(C2=CC3=C(C(=C([N-]3)C=C4C(=C(C(=N4)C=C5C(=C(C(=N5)C=C1[N-]2)C)C=C)C)C=C)C)CCC(=O)[O-])CCC(=O)[O-].[Fe]'], 
#         ['P0DP24_boltz_p3', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC', 'CC1=C(C2=CC3=C(C(=C([N-]3)C=C4C(=C(C(=N4)C=C5C(=C(C(=N5)C=C1[N-]2)C)C=C)C)C=C)C)CCC(=O)[O-])CCC(=O)[O-].[Fe]'],
#         ['P0DP24_boltz_p4', 'MALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAAMALWMRLLPLLALLALWGPDPAAA', 'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC', 'CC1=C(C2=CC3=C(C(=C([N-]3)C=C4C(=C(C(=N4)C=C5C(=C(C(=N5)C=C1[N-]2)C)C=C)C)C=C)C)CCC(=O)[O-])CCC(=O)[O-].[Fe]']]
# df = pd.DataFrame(rows, columns=[id_col, seq_col, substrate_col, intermediate_col])
# df = df.head(2)
# df[intermediate_col] = None
# df << (Boltz(id_col, seq_col, substrate_col, intermediate_col, f'{output_dir}', num_threads) >> Save(f'{output_dir}test.pkl'))
