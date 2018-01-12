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

setup(
    name = "epigeec",
    version = "1.0",
    author = "Jonathan Laperle",
    author_email = "jonathan.laperle@usherbrooke.ca",
    description = ("Tools for fast NxN correlation of whole-genome epigenomic data."),
    packages = find_packages(),
    package_data = {'epigeec': ['bin/bg_to_hdf5',
                               'bin/bw_to_hdf5',
                               'bin/correlation',
                               'bin/filter']},
    entry_points = {'console_scripts': ['epigeec = epigeec.python.core.main:main']},
    install_requires = ["pandas", "numpy", "wheel"],
    license = "GPL",
    python_requires = '>=2.6, <3',
    long_description = open("README.rst").read()
)
