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

VERSION = "1.2"

EPI_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
BIN_DIR = os.path.join(EPI_DIR, "bin")
BW_TO_HDF5_PATH = os.path.join(BIN_DIR, "bw_to_hdf5")
BG_TO_HDF5_PATH = os.path.join(BIN_DIR, "bg_to_hdf5")
FILTER_PATH = os.path.join(BIN_DIR, "filter")
CORR_PATH = os.path.join(BIN_DIR, "correlation")
