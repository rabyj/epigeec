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

import os.path

#directories
MODULE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

#executables
def exec_path(exec_name):
    return os.path.join(os.path.dirname(MODULE_DIR), 'bin', exec_name)

BW_TO_HDF5 = exec_path('bw_to_hdf5')
BG_TO_HDF5 = exec_path('bg_to_hdf5')
FILTER = exec_path('filter')
CORRELATION = exec_path('correlation')
MAKE_MATRIX = exec_path('make_matrix')

#chrom sizes
def chrom_sizes_path_maker(filename):
    return os.path.join(os.path.dirname(MODULE_DIR),'resource','chrom_sizes',filename)

def get_chrom_sizes(assembly):
    assembly = assembly.lower()
    if assembly != 'saccer3':
        assembly = assembly + '.noy'
    else:
        assembly = assembly + '.can'
    filename = '{0}.chrom.sizes'.format(assembly)
    return chrom_sizes_path_maker(filename)

#regions
def region_path_maker(filename):
    return os.path.join(os.path.dirname(MODULE_DIR), 'resource', 'filter', filename)

def get_region(assembly, content):
    if content == 'none':
        return region_path_maker('none.bed')
    filename = "{0}.{1}.bed".format(assembly.lower(), content.lower())
    return region_path_maker(filename)

def get_resolution(num):
    to_human = {1:"1bp",
                10:"10bp",
                100: "100bp",
                1000: "1kb",
                10000: "10kb",
                100000: "100kb",
                1000000: "1mb",
                10000000: "10mb",
                100000000: "100mb"}
    return to_human[int(num)]
