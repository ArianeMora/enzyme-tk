from enzymetk.annotateEC_CLEAN_step import CLEAN
from enzymetk.save_step import Save
import pandas as pd

output_dir = '/disk1/ariane/vscode/enzyme-tk/examples/tmp/'
num_threads = 1
id_col = 'Entry'
seq_col = 'Sequence'
substrate_col = 'Substrate'
rows = [['AXE2', 'MKIGSGEKLLFIGDSITDCGRARPEGEGSFGALGTGYVAYVVGLLQAVYPELGIRVVNKGISGNTVRDLKARWEEDVIAQKPDWVSIMIGINDVWRQYDLPFMKEKHVYLDEYEATLRSLVLETKPLVKGIILMTPFYIEGNEQDPMRRTMDQYGRVVKQIAEETNSLFVDTQAAFNEVLKTLYPAALAWDRVHPSVAGHMILARAFLREIGFEWVRSR', 
         'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC'], 
        ['H7C0D0', 'XRAHREIKDIFYKAIQKRRQSQEKIDDILQTLLDATYKDGRPLTDDEVAGMLIGLLLAGQHTSSTTSAWMGFFLARDKTLQKKCYLEQKTVCGENLPPLTYDQLKDLNLLDRCIKETLRLRPPIMIMMRMARTPQTVAGYTIPPGHQDNPASGEKFAYVPFGAGRHRCIGENFAYVQIKTIWSTMLRLYEFDLIDGYFPTVNYTTMIHTPENPVIRYKRRSK', 
         'CCCCC(CC)COC(=O)C1=CC=CC=C1C(=O)OCC(CC)CCCC']]
df = pd.DataFrame(rows, columns=[id_col, seq_col, substrate_col])
# This should be relative to the location of the script if you installed via the install_all.sh script
clean_dir = '/disk1/share/software/CLEAN/app/'

# Note! You cannot have underscores in the sample name (presumably no funky characters)
df << (CLEAN(id_col, seq_col, clean_dir, num_threads=1) >> Save(f'{output_dir}clean_test.pkl'))