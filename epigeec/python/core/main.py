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
                 args.signal_file,
                 args.chrom_sizes,
                 args.resolution,
                 args.output_hdf5]
    subprocess.call(command)

def hdf5_filter(args):
    if args.include:
        include = args.include
    else:
        include = tmp_name()
        make_all_filter(open(include, 'w'), open(args.chrom_sizes))
    if args.exclude:
        exclude = args.exclude
    else:
        exclude = tmp_name()
        open(exclude, 'w')
    command = [FILTER_PATH,
                 args.hdf5,
                 args.chrom_sizes,
                 args.resolution,
                 args.output_hdf5,
                 include,
                 exclude]
    subprocess.call(command)

def corr(args):
    corr_path = tmp_name()
    #call correlation
    command = [CORR_PATH,
                 args.hdf5_list,
                 args.chrom_sizes,
                 args.resolution,
                 corr_path]
    subprocess.call(command)

    #call make_matrix
    make_matrix.main(args.hdf5_list, corr_path, args.output_matrix)
    subprocess.call(command)

def make_parser():
    parser = argparse.ArgumentParser(description = "EpiGeEC - Tools for fast NxN correlation of deep sequencing data")
    subparsers = parser.add_subparsers(help = "sub-command help")

    parser_hdf5 = subparsers.add_parser("to_hdf5", help="Convert a signal file format to a more efficient hdf5 format for use with other epiGeEC tools")
    parser_hdf5.set_defaults(func=to_hdf5)
    group = parser_hdf5.add_mutually_exclusive_group(required=True)
    group.add_argument("-bw", "--bigwig", action='store_true', help="use this flag for a bigwig file")
    group.add_argument("-bg", "--bedgraph", action='store_true', help="use this flag for a bedgraph file")
    parser_hdf5.add_argument("signal_file", help="signal file (bigwig or bedgraph")
    parser_hdf5.add_argument("chrom_sizes", help="chrom_sizes of the assembly, chromosomes not in this file will be ignored")
    parser_hdf5.add_argument("resolution", help="resolution of the binning (1kb to 1mb prefered for human)")
    parser_hdf5.add_argument("output_hdf5", help="output file (hdf5)")

    parser_filter = subparsers.add_parser("filter", help="Select regions to be kept or removed from an hdf5 file, this step is optional")
    parser_filter.set_defaults(func=hdf5_filter)
    parser_filter.add_argument("hdf5", help="hdf5 file to be filtered")
    parser_filter.add_argument("chrom_sizes", help="chrom_sizes of the assembly, chromosomes not in this file will be ignored")
    parser_filter.add_argument("resolution", help="resolution of the binning (1kb to 1mb prefered for human)")
    parser_filter.add_argument("output_hdf5", help="output file (hdf5)")
    parser_filter.add_argument("--include", "-i", help="bed file of regions to keep(exclude wins in case of conflict with include)")
    parser_filter.add_argument("--exclude", "-e", help="bed file of resions to remove(exclude wins in case of conflict with include)")

    parser_corr = subparsers.add_parser("correlation", help="Perform N by N pearson correlation of hdf5 files, must be same assembly, filter and resolution")
    parser_corr.set_defaults(func=corr)
    parser_corr.add_argument("hdf5_list", help="list of hdf5 files to correlate, one file per line")
    parser_corr.add_argument("chrom_sizes", help="chrom_sizes of the assembly, chromosomes not in this file will be ignored")
    parser_corr.add_argument("resolution", help="resolution of the binning (1kb to 1mb prefered for human)")
    parser_corr.add_argument("output_matrix", help="final tsv matrix file with every correlation result")
   
    return parser

 
def main():
    parser = make_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
