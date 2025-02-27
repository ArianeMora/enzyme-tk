import sys
sys.path.append('../enzymetk/')
from steps.predict_catalyticsite_step import ActiveSitePred
from steps.save_step import Save
import pandas as pd
import os
os.environ['MKL_THREADING_LAYER'] = 'GNU'

# This should be where you downloaded the data from zotero, there is a folder in there called AS_inference
# This contains the models and the data needed to run the tool
#squidly_dir = '/disk1/share/software/AS_inference/'
squidly_dir = '/disk1/ariane/vscode/enzyme-tk/models/squidly_final_models/15B/'
num_threads = 1
id_col = 'Entry'
seq_col = 'Sequence'
rows = [['AXE2', 'MKIGSGEKLLFIGDSITDCGRARPEGEGSFGALGTGYVAYVVGLLQAVYPELGIRVVNKGISGNTVRDLKARWEEDVIAQKPDWVSIMIGINDVWRQYDLPFMKEKHVYLDEYEATLRSLVLETKPLVKGIILMTPFYIEGNEQDPMRRTMDQYGRVVKQIAEETNSLFVDTQAAFNEVLKTLYPAALAWDRVHPSVAGHMILARAFLREIGFEWVRSR'], 
        ['H7C0D0', 'XRAHREIKDIFYKAIQKRRQSQEKIDDILQTLLDATYKDGRPLTDDEVAGMLIGLLLAGQHTSSTTSAWMGFFLARDKTLQKKCYLEQKTVCGENLPPLTYDQLKDLNLLDRCIKETLRLRPPIMIMMRMARTPQTVAGYTIPPGHQDNPASGEKFAYVPFGAGRHRCIGENFAYVQIKTIWSTMLRLYEFDLIDGYFPTVNYTTMIHTPENPVIRYKRRSK']]
df = pd.DataFrame(rows, columns=[id_col, seq_col])
print(df)
df << (ActiveSitePred(id_col, seq_col, squidly_dir, num_threads) >> Save('tmp/squidly_as_pred.pkl'))
