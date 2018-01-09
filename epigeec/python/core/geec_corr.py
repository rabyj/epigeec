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


def tmp_name():
    fd, temp_path = tempfile.mkstemp()
    os.close(fd)
    os.remove(temp_path)
    return temp_path

def correlation(input_file, corr_path, mat_path):
    assembly = geec_config["assembly"]
    include = config.get_region(assembly, geec_config["include"])
    exclude = config.get_region(assembly, geec_config["exclude"])
    resolution = geec_config["resolution"]
    chrom_sizes = config.get_chrom_sizes(assembly)

    input_path = tmp_name()
    corr_input_file = open(input_path, 'w')
    for line in input_file:
        name = line.strip()
        filtered_name = "{0}_{1}_{2}_{3}.hdf5".format(name, config.get_resolution(resolution), geec_config["include"], geec_config["exclude"])
        filtered_hdf5 = os.path.join(geec_config["filtered_folder"], filtered_name)
        corr_input_file.write("{0}\t{1}\n".format(filtered_hdf5, name))
    corr_input_file.close()
    
    correlate(input_path, chrom_sizes, corr_path, resolution)
    make_matrix(input_path, corr_path, mat_path)
    
def main():
    list_path = sys.argv[1]
    corr_path = geec_config["corr_path"]
    mat_path = geec_config["mat_path"]
    correlation(open(list_path), corr_path, mat_path)

if __name__ == '__main__':
    geec_config = load_config(sys.argv[2])
    main()

