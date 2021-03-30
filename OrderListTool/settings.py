# Copyright (C) 2021 Matthias Schaefer
# 
# This file is part of OrderListTool.
# 
# OrderListTool is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# OrderListTool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with OrderListTool.  If not, see <http://www.gnu.org/licenses/>.

# default settings
DEFAULT_SYSTEM = "KiCAD"

# reference symbols to ignore, because there belongs no part to them (i.e. holes, test pins)
# independent from CAD system
REF_SYM_IGNORE = []
# order of BOMKW_REQ_PROPERTIES has to be equal to order of BOMKW_PART_PROPERTIES (see definitions.py)!
# here, user has to list, how the property mentioned in BOMKW_PART_PROPERTIES are named in the csv-file
# usually, this depends on CAD system (see below).
BOMKW_REQ_PROPERTIES = []

# CAD system depending definitions
SYSTEMS = []
# KiCAD
SYSTEMS.append({
    "NAME":"KiCAD",
    "REF_SYM_IGNORE":["H","TP"],
    # mapped to BOMKW_PART_PROPERTIES
    # i.e. in KiCAD the "package" is named "footprint"
    "BOMKW_REQ_PROPERTIES":["ref", "value", "footprint"]
})
# EAGLE
SYSTEMS.append({
    "NAME":"EAGLE",
    "REF_SYM_IGNORE":["TP"],
    # mapped to BOMKW_PART_PROPERTIES
    "BOMKW_REQ_PROPERTIES":["part", "value", "package"]
})
