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

import itertools
import multiprocessing
import os
import subprocess
import sys
import tempfile

import config
from geec_tools import *

def process_unit(args):
    """
    """
    try:
        name, chrom_sizes, user_hdf5, filtered_hdf5, resolution, include, exclude = args
        filter_hdf5(name, chrom_sizes, user_hdf5, filtered_hdf5, resolution, include, exclude)
    except:
        pass


def make_args(list_file, assembly, resolution):
    include = config.get_region(assembly, geec_config["include"])
    exclude = config.get_region(assembly, geec_config["exclude"])
    chrom_sizes = config.get_chrom_sizes(assembly)

    args_list=[]
    for line in list_file:
        name = line.strip()
        hdf5_name = "{0}_{1}_{2}_{3}.hdf5".format(name, config.get_resolution(resolution) , "all", "none")
        filtered_name = "{0}_{1}_{2}_{3}.hdf5".format(name, config.get_resolution(resolution) , geec_config["include"], geec_config["exclude"])
        user_hdf5 = os.path.join(geec_config["hdf5_folder"], hdf5_name)
        filtered_hdf5 = os.path.join(geec_config["filtered_folder"], filtered_name)
        args = (name, chrom_sizes,
                user_hdf5, filtered_hdf5, resolution,
                include, exclude)
        args_list.append(args)
    return args_list

def hdf5_filter(list_path):
    assembly = geec_config["assembly"]
    resolution = geec_config["resolution"]
    args_list = make_args(open(list_path), assembly, resolution)
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    try:
        pool.map(process_unit, args_list)
    except KeyboardInterrupt:
        pool.terminate()
        exit(1)

def main():
    """
    """
    list_path = sys.argv[1]
    hdf5_filter(list_path)

if __name__ == '__main__':
    geec_config = load_config(sys.argv[2])
    main()
