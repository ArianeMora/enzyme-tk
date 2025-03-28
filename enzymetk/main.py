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
Date: September 2024
"""
from enzymetk import *
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Run on a dataframe")
    parser.add_argument('-out', '--out', required=True, help='Path to the output directory')
    parser.add_argument('-df', '--df', type=str, required=True, help='Fasta of the file of interest')
    return parser.parse_args()

def main():
    args = parse_args()
    #run(args.out, args.df)

if __name__ == "__main__":
    main()