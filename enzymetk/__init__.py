###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

"""
Author: Ariane Mora
Date: March 2025
"""
__title__ = 'enzymetk'
__description__ = 'Toolkit for enzymes and what not'
__url__ = 'https://github.com/arianemora/enzyme-tk/'
__version__ = '0.0.7'
__author__ = 'Ariane Mora'
__author_email__ = 'ariane.n.mora@gmail.com'
__license__ = 'GPL3'


# Core classes
from enzymetk.step import Step, Pipeline
from enzymetk.save_step import Save

# EC Annotation
from enzymetk.annotateEC_CLEAN_step import CLEAN
from enzymetk.annotateEC_CREEP_step import CREEP
from enzymetk.annotateEC_proteinfer_step import ProteInfer

# Docking
from enzymetk.dock_boltz_step import Boltz
from enzymetk.dock_chai_step import Chai
from enzymetk.dock_vina_step import Vina

# Chemical Embeddings
from enzymetk.embedchem_chemberta_step import ChemBERT
from enzymetk.embedchem_rxnfp_step import RxnFP
from enzymetk.embedchem_selformer_step import SelFormer
from enzymetk.embedchem_unimol_step import UniMol

# Protein Embeddings
from enzymetk.embedprotein_esm_step import EmbedESM
from enzymetk.embedprotein_esm3_step import EmbedESM3

# Sequence Generation/Alignment
from enzymetk.generate_msa_step import ClustalOmega
from enzymetk.generate_tree_step import FastTree

# Protein Design
from enzymetk.inpaint_ligandMPNN_step import LigandMPNN

# Metagenomics
from enzymetk.metagenomics_porechop_trim_reads_step import PoreChop
from enzymetk.metagenomics_prokka_annotate_genes import Prokka

# Prediction
from enzymetk.predict_catalyticsite_step import ActiveSitePred

# Sequence Search
from enzymetk.sequence_search_blast import BLAST

# Similarity Search
from enzymetk.similarity_foldseek_step import FoldSeek
from enzymetk.similarity_mmseqs_step import MMseqs
from enzymetk.similarity_reaction_step import ReactionDist
from enzymetk.similarity_substrate_step import SubstrateDist

# Structure Search (aliased to avoid conflict with similarity_foldseek_step.FoldSeek)
from enzymetk.structure_search_foldseek import FoldSeek as StructureFoldSeek


__all__ = [
    # Core
    'Step',
    'Pipeline', 
    'Save',
    # EC Annotation
    'CLEAN',
    'CREEP',
    'ProteInfer',
    # Docking
    'Boltz',
    'Chai',
    'Vina',
    # Chemical Embeddings
    'ChemBERT',
    'RxnFP',
    'SelFormer',
    'UniMol',
    # Protein Embeddings
    'EmbedESM',
    'EmbedESM3',
    # Sequence Generation/Alignment
    'ClustalOmega',
    'FastTree',
    # Protein Design
    'LigandMPNN',
    # Metagenomics
    'PoreChop',
    'Prokka',
    # Prediction
    'ActiveSitePred',
    # Sequence Search
    'BLAST',
    # Similarity Search
    'FoldSeek',
    'MMseqs',
    'ReactionDist',
    'SubstrateDist',
    # Structure Search
    'StructureFoldSeek',
]
