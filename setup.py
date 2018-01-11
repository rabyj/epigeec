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

import os
from setuptools import setup, find_packages

setup(
    name = "epigeec",
    version = "0.9",
    author = "Jonathan Laperle",
    author_email = "jonathan.laperle@usherbrooke.ca",
    description = ("TODO"),
    packages = find_packages(),
    #data_files = [('bin', ['epigeec/bin/*'])]
    entry_points = {'console_scirpts': ['epigeec = epigeec.python.core.main:main']},
    install_requires = ["pandas", "numpy", "wheel"],
    license = "GPL",
    python_requires='>=2.6, <3'
)
