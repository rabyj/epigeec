#!/usr/bin/env python2
# Copyright (C) 2015 Jonathan Laperle. All Rights Reserved.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================

import argparse
import logging
import os.path
import subprocess
import sys
import tempfile

import make_matrix

EPI_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
BIN_DIR = os.path.join(EPI_DIR, "bin")
BW_TO_HDF5_PATH = os.path.join(BIN_DIR, "bw_to_hdf5")
BG_TO_HDF5_PATH = os.path.join(BIN_DIR, "bg_to_hdf5")
FILTER_PATH = os.path.join(BIN_DIR, "filter")
CORR_PATH = os.path.join(BIN_DIR, "correlation")

def tmp_name():
    fd, temp_path = tempfile.mkstemp()
    os.close(fd)
    os.remove(temp_path)
    return temp_path

def make_all_filter(tmp, chrom):
    for line in chrom:
       line = line.strip()
       if line:
           line = line.split()
           tmp.write("{0}\t{1}\t{2}\n".format(line[0], "0", line[1]))

def get_hdf5_converter(args):
    if args.bigwig:
        exe = BW_TO_HDF5_PATH
    elif args.bedgraph:
        exe = BG_TO_HDF5_PATH
    else:
        print "No file type switch provided use -bg or -bw"
        sys.exit(1)
    return exe

def to_hdf5(args):
    exe = get_hdf5_converter(args)
    command = [exe,
                 args.signalFile,
                 args.chromSizes,
                 args.resolution,
                 args.outHdf5]
    subprocess.call(command)

def hdf5_filter(args):
    if args.select:
        select = args.select
    else:
        select = tmp_name()
        make_all_filter(open(select, 'w'), open(args.chromSizes))
    if args.exclude:
        exclude = args.exclude
    else:
        exclude = tmp_name()
        open(exclude, 'w')
    command = [FILTER_PATH,
                 args.hdf5,
                 args.chromSizes,
                 args.resolution,
                 args.outHdf5,
                 select,
                 exclude]
    subprocess.call(command)

def corr(args):
    corr_path = tmp_name()
    #call correlation
    command = [CORR_PATH,
                 args.hdf5List,
                 args.chromSizes,
                 args.resolution,
                 corr_path]
    subprocess.call(command)

    #call make_matrix
    make_matrix.main(args.hdf5List, corr_path, args.outMatrix)
    subprocess.call(command)

def make_parser():
    parser = argparse.ArgumentParser(prog='epiGeEC', description = "EpiGeEC - Tools for fast NxN correlation of deep sequencing signal data")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.9')
    subparsers = parser.add_subparsers(help = "Sub-command help.") #TODO submod summary

    parser_hdf5 = subparsers.add_parser("to_hdf5", description="Average the singla in non-overlapping bins." ,help="Convert a signal file format to a more efficient hdf5 format for use with other epiGeEC tools.")
    parser_hdf5.set_defaults(func=to_hdf5)
    group = parser_hdf5.add_mutually_exclusive_group(required=True)
    group.add_argument("-bw", "--bigwig", action='store_true', help="Indicate that the signal file is in bigWig format.")
    group.add_argument("-bg", "--bedgraph", action='store_true', help="Indicate that the signal file is in bedGraph format.")
    parser_hdf5.add_argument("signalFile", help="The signal file, bigWig or bedGraph. (TEXT)")
    parser_hdf5.add_argument("chromSizes", help="Chromosome sizes of the assembly, chromosomes not in this file are ignored. (TEXT)")
    parser_hdf5.add_argument("resolution", help="The resolution of the binning in base pair (1kb suggested for human). (INTEGER)")
    parser_hdf5.add_argument("outHdf5", help="The output file. (TEXT)")

    parser_filter = subparsers.add_parser("filter", description="Select or remove bins of a HDF5 file." ,help="Select regions to be kept or removed from a HDF5 file (this step is optional).")
    parser_filter.set_defaults(func=hdf5_filter)
    parser_filter.add_argument("hdf5", help="The HDF5 file to be filtered. (TEXT)")
    parser_filter.add_argument("chromSizes", help="Chromosome sizes of the assembly, chromosomes not in this file are ignored. (TEXT)")
    parser_filter.add_argument("resolution", help="The resolution of the binning in base pair (1kb suggested for human). (INTEGER)")
    parser_filter.add_argument("outHdf5", help="The output file. (TEXT)")
    parser_filter.add_argument("--select", "-s", help="The file in BED format containing the regions to select, others are ignored. In case a region is both selected and excluded, the exclusion dominates. (TEXT)")
    parser_filter.add_argument("--exclude", "-e", help="The file in BED format containing the regions to exclude.")

    parser_corr = subparsers.add_parser("correlate", description="Compute a Pearson correlation coefficient for each pair of hdf5 from a list.", help="Perform N by N Pearson correlation of HDF5 files generated with the same chrom sizes, filters and resolution.")
    parser_corr.set_defaults(func=corr)
    parser_corr.add_argument("hdf5List", help="The list of HDF5 files to correlate, one file per line. (TEXT)")
    parser_corr.add_argument("chromSizes", help="Chromosome sizes of the assembly, chromosomes not in this file are ignored. (TEXT)")
    parser_corr.add_argument("resolution", help="The resolution of the binning in base pair (1kb suggested for human). (INTEGER)")
    parser_corr.add_argument("outMatrix", help="The final tab-delimited matrix file. (TEXT)")
   
    return parser

 
def main():
    parser = make_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
