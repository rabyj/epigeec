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

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False
except ImportError:
    bdist_wheel = None

setup(
    name = "epigeec",
    version = "0.9",
    author = "Jonathan Laperle",
    author_email = "jonathan.laperle@usherbrooke.ca",
    description = ("Tools for fast NxN correlation of whole-genome epigenomic data."),
    packages = find_packages(),
    entry_points = {'console_scirpts': ['epigeec = epigeec.python.core.main:main']},
    install_requires = ["pandas", "numpy", "wheel"],
    license = "GPL",
    python_requires = '>=2.6, <3',
    long_description = open("README.rst").read(),
    cmdclass={'bdist_wheel': bdist_wheel}
)
