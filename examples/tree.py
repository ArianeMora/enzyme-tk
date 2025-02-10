from steps.generate_tree_step import FastTree
from steps.save_step import Save
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Define paths
fasttree_dir = '/home/ikumi/degradeo/software/'
csv_file = '/home/ikumi/degradeo/pipeline/ikumi_data/Q04457_esterase-2.csv'
output_dir = '/home/ikumi/degradeo/pipeline/ikumi_data/'

# Initialize FastTree   
fast_tree = FastTree(
    fasttree_dir=fasttree_dir,
    id_col='Entry',
    seq_col='Sequence',
    csv_file=csv_file,
    output_dir=output_dir
)

# Read the CSV file instead of using undefined 'rows'
df = pd.read_csv(csv_file)
df << (fast_tree >> Save(f'{output_dir}Q04457_esterase-2.pkl'))