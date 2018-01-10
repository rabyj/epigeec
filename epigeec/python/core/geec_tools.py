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

import subprocess

import config

def load_config(stream):
    config = {}
    for line in open(stream):
        line = line.strip()
        if line:
            line = line.split('=')
            config[line[0].strip()] = line[1].strip()
    return config

def bw_to_hdf5(raw_file, name, chrom_sizes, user_hdf5, resolution):
    """Usage: to_hdf5 {dataset.bw}
                      {name}
                      {chrom_sizes}
                      {output.hdf5}
                      {bin_size}\n"""
    subprocess.call([config.BW_TO_HDF5,
                     raw_file,
                     name,
                     chrom_sizes,
                     user_hdf5,
                     resolution])

def bg_to_hdf5(raw_file, name, chrom_sizes, user_hdf5, resolution):
    """Usage: to_hdf5 {dataset.bw}
                      {name}
                      {chrom_sizes}
                      {output.hdf5}
                      {bin_size}\n"""
    subprocess.call([config.BG_TO_HDF5,
                     raw_file,
                     name,
                     chrom_sizes,
                     user_hdf5,
                     resolution])

def filter_hdf5(name, chrom_sizes, user_hdf5, filtered_hdf5, resolution, include, exclude):
    """Usage: filter    {input.hdf5}
                        {name}
                        {output.hdf5}
                        {chrom_sizes}
                        {bin_size}
                        {include.bed}
                        {exclude.bed}\n");"""
    subprocess.call([config.FILTER,
                     user_hdf5,
                     name,
                     filtered_hdf5,
                     chrom_sizes,
                     resolution,
                     include,
                     exclude
                    ])


def correlate(input_list, chrom_sizes, correlation_file, resolution):
    """Usage: correlation {input_list}
                          {chrom_sizes}
                          {output.results}
                          {bin_size}\n");"""
    subprocess.call([config.CORRELATION,
                     input_list,
                     chrom_sizes,
                     correlation_file,
                     resolution
                     ])

def correlate_nm(input_list1, input_list2, chrom_sizes, correlation_file, resolution):
    """Usage: correlation_nm {input_list1}
                             {input_list2}
                             {chrom_sizes}
                             {output.results}
                             {bin_size}\n");"""
    subprocess.call([config.CORRELATION_NM,
                     input_list1,
                     input_list2,
                     chrom_sizes,
                     correlation_file,
                     resolution
                     ])

def make_matrix(input_list, correlation_file, output_matrix):
    """
    python make_matrix.py {list_path} {chrom_size} {corr_path} {output_path}
    """
    subprocess.call(['python', 
                     config.MAKE_MATRIX,
                     input_list,
                     correlation_file,
                     output_matrix
                     ])

def make_matrix_nm(input_list1, input_list2, correlation_file, precalc_matrix, output_matrix):
    """
    python make_matrix.py {list_path} {chrom_size} {corr_path} {output_path}
    """
    subprocess.call(['python',
                     config.MAKE_MATRIX_NM,
                     input_list1,
                     input_list2,
                     correlation_file,
                     precalc_matrix,
                     output_matrix
                     ])
