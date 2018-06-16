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
from setuptools import setup, find_packages

import epigeec.python.core.config as config

setup(
    name = "epigeec",
    version = config.VERSION,
    author = "Jonathan Laperle",
    author_email = "jonathan.laperle@usherbrooke.ca",
    description = ("Tools for fast NxN correlation of whole-genome epigenomic data."),
    packages = find_packages(),
    package_data = {'epigeec': ['bin/bg_to_hdf5',
                                'bin/bw_to_hdf5',
                                'bin/correlation',
                                'bin/correlation_w',
                                'bin/filter',
                                'lib/libboost_container.so.1.61.0',
                                'lib/libboost_filesystem.so.1.61.0',
                                'lib/libboost_iostreams.so.1.61.0',
                                'lib/libboost_system.so.1.61.0',
                                'lib/libbwreader.so',
                                'lib/libcore.so',
                                'lib/libgomp.so.1',
                                'lib/libhdf5.so.10',
                                'lib/libhdf5_hl.so.10',
                                'lib/libimf.so',
                                'lib/libintlc.so.5',
                                'lib/libstdc++.so.6',
                                'lib/libsvml.so',
                                'lib/libsz.so.2',
                                'lib/libz.so.1',
                                'test/files/signal/d9f18e91644bacfee3669d577b661d15',
                                'test/files/signal/fd85fe6672c629a116a9b6131883a60b',
                                'test/files/signal/001f63cdf00286183e32c1bb0fd6d85f',
                                'test/files/signal/002f4247fadb6c6e4000a6fc12e5b93a',
                                'test/files/hdf5/test.hdf5',
                                'test/files/expected',
                                'test/files/expected_w',
                                'test/files/expected_hg19',
                                'resource/chrom_sizes/saccer3.can.chrom.sizes',]},
    entry_points = {'console_scripts': ['epigeec = epigeec.python.core.main:cli']},
    install_requires = ["pandas", "numpy", "wheel", "h5py", "future"],
    license = "GPL",
    long_description = open("README.rst").read()
)
