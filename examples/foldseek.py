import sys

from enzymetk.similarity_foldseek_step import FoldSeek
from enzymetk.save_step import Save
import pandas as pd


# id_col: str, seq_col: str, proteinfer_dir: str,
output_dir = 'tmp/'
rows = [['P0DP24_3', 'tmp/P0DP24/chai/P0DP24_3.cif'],
        ['P0DP24_1', 'tmp/P0DP24/chai/P0DP24_1.cif']]
df = pd.DataFrame(rows, columns=['id', 'pdbs'])
# foldseek_dir: str, pdb_column_name: str, reference_database: str
reference_database = '/disk4/share/software/foldseek/structures/pdb/pdb'
#df << (FoldSeek('id', 'pdbs', reference_database) >> Save(f'{output_dir}pdb_files.pkl'))
#df << (FoldSeek('id', 'pdbs', reference_database, method='cluster', tmp_dir='tmp/') >> Save(f'{output_dir}pdb_files.pkl'))


# id_col: str, seq_col: str, proteinfer_dir: str,
id_col = 'Entry'
seq_col = 'Sequence'
label_col = 'label'
output_dir = 'tmp/'
rows = [['AXE2_TALPU', 'query', 'MHSKFFAASLLGLGAAAIPLEGVMEKRSCPAIHVFGARETTASPGYGSSSTVVNGVLSAYPGSTAEAINYPACGGQSSCGGASYSSSVAQGIAAVASAVNSFNSQCPSTKIVLVGYSQGGEIMDVALCGGGDPNQGYTNTAVQLSSSAVNMVKAAIFMGDPMFRAGLSYEVGTCAAGGFDQRPAGFSCPSAAKIKSYCDASDPYCCNGSNAATHQGYGSEYGSQALAFVKSKLG'],
        ['AXE2_TALPU', 'reference', 'MHSKFFAASLLGLGAAAIPLEGVMEKRSCPAIHVFGARETTASPGYGSSSTVVNGVLSAYPGSTAEAINYPACGGQSSCGGASYSSSVAQGIAAVASAVNSFNSQCPSTKIVLVGYSQGGEIMDVALCGGGDPNQGYTNTAVQLSSSAVNMVKAAIFMGDPMFRAGLSYEVGTCAAGGFDQRPAGFSCPSAAKIKSYCDASDPYCCNGSNAATHQGYGSEYGSQALAFVKSKLG'],
        ['AXE2_GEOSE', 'reference', 'MKIGSGEKLLFIGDSITDCGRARPEGEGSFGALGTGYVAYVVGLLQAVYPELGIRVVNKGISGNTVRDLKARWEEDVIAQKPDWVSIMIGINDVWRQYDLPFMKEKHVYLDEYEATLRSLVLETKPLVKGIILMTPFYIEGNEQDPMRRTMDQYGRVVKQIAEETNSLFVDTQAAFNEVLKTLYPAALAWDRVHPSVAGHMILARAFLREIGFEWVRSR'], 
        ['AXE7A_XYLR2', 'referece', 'MFNFAPKQTTEMKKLLFTLVFVLGSMATALAENYPYRADYLWLTVPNHADWLYKTGERAKVEVSFCLYGMPQNVEVAYEIGPDMMPATSSGKVTLKNGRAVIDMGTMKKPGFLDMRLSVDGKYQHHVKVGFSPELLKPYTKNPQDFDAFWKANLDEARKTPVSVSCNKVDKYTTDAFDCYLLKIKTDRRHSIYGYLTKPKKAGKYPVVLCPPGAGIKTIKEPMRSTFYAKNGFIRLEMEIHGLNPEMTDEQFKEITTAFDYENGYLTNGLDDRDNYYMKHVYVACVRAIDYLTSLPDWDGKNVFVQGGSQGGALSLVTAGLDPRVTACVANHPALSDMAGYLDNRAGGYPHFNRLKNMFTPEKVNTMAYYDVVNFARRITCPVYITWGYNDNVCPPTTSYIVWNLITAPKESLITPINEHWTTSETNYTQMLWLKKQVK'], 
        ['A0A0B8RHP0_LISMN', 'reference', 'MKKLLFLGDSVTDAGRDFENDRELGHGYVKIIADQLEQEDVTVINRGVSANRVADLHRRIEADAISLQPDVVTIMIGINDTWFSFSRWEDTSVTAFKEVYRVILNRIKTETNAELILMEPFVLPYPEDRKEWRGDLDPKIGAVRELAAEFGATLIPLDGLMNALAIKHGPTFLAEDGVHPTKAGHEAIASTWLEFTK']]
df = pd.DataFrame(rows, columns=[id_col, label_col, seq_col])
# foldseek_dir: str, pdb_column_name: str, reference_database: str
reference_database = '/disk4/share/software/foldseek/structures/pdb/pdb'
#df << (FoldSeek(id_col, seq_col, reference_database, query_type='seqs',  method='cluster') >> Save(f'{output_dir}pdb_files_seqs.pkl'))
# foldseek_dir: str, pdb_column_name: str, reference_database: str
# #df << (FoldSeek('id', 'pdbs', reference_database) >> Save(f'{output_dir}pdb_files.pkl'))
df << (FoldSeek(id_col, seq_col, reference_database, query_type='seqs',  tmp_dir='tmp/') >> Save(f'{output_dir}pdb_files.pkl'))
