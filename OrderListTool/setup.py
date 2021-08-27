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

# default configuration
###################################################################################################
DEFAULT_DIRECTORY = ""  # preselect folder containing database files
DEFAULT_FILE = ""       # preselect a BOM-file
LANGUAGE = "de"         # GUI language (en, de)

# define part template instances (PTI)
###################################################################################################
# list all properties, that each instance must have
# for proper function of this tool, this list must contain as a minimum: ["value", "ordNum", "package", "distributor", "manNum"]
PTI_REQ_PROPERTIES = ["value", "ordNum", "package", "distributor", "manNum"]

# parts found in the bom file, which will not match to one of the listed instances below,
# will be collected in an instance called "others"
# database files, containing keywords not assigned to any of the instances below,
# will be treated as others
PTI = []
# capacitor
PTI.append({
    "part_type":"capacitor",
    "requested_properties":["value", "ordNum", "distributor", "package", "voltage", "dielectric", "tolerance", "manNum"],
    "reference_symbols":["C"],
    "keyword_database_file":"capacitor",
    "description":"Kapazitäten"
})
# inductor
PTI.append({
    "part_type":"inductor",
    "requested_properties":["value", "ordNum", "distributor", "package", "current", "tolerance", "manNum"],
    "reference_symbols":["L"],
    "keyword_database_file":"inductor",
    "description":"Induktivitäten"
})
# resistor
PTI.append({
    "part_type":"resistor",
    "requested_properties":["value", "ordNum", "distributor", "package", "power", "tolerance", "manNum"],
    "reference_symbols":["R","RV"],
    "keyword_database_file":"resistor",
    "description":"Widerstände"
})
# semiconductor
PTI.append({
    "part_type":"semiconductor",
    "requested_properties":["value", "ordNum", "distributor", "package", "manNum"],
    "reference_symbols":["D","Q"],
    "keyword_database_file":"semiconductor",
    "description":"Halbleiter"
})
# mechanics
PTI.append({
    "part_type":"mechanics",
    "requested_properties":["value", "ordNum", "distributor", "package", "manNum"],
    "reference_symbols":["J","JP","F","K"],
    "keyword_database_file":"mechanics",
    "description":"mechanische Bauteile"
})
# ICs
PTI.append({
    "part_type":"ic",
    "requested_properties":["value", "ordNum", "distributor", "package", "manNum"],
    "reference_symbols":["U"],
    "keyword_database_file":"circuit",
    "description":"IC's"
})
# defalut category "others" will be created automatically and doesn't need to be defined here

# distributor order list configuration (DOC)
###################################################################################################
# create one configuration for each dedicated distributor
# distribitors found in the database files and not listed here, will be summarized in a default output file
#   - list all information, that are requested when generating the list of ordering numbers
#       - each property (except of "ref" and "qnty") listed below also has to be mentioned in the PTI_REQ_PROPERTIES (see above)
#       - property "qnty" is provided by the program, only use it, it must not be defined in PTI_REQ_PROPERTIES (see above)
#   - decide whether to get a header containing the property names in the output file or not
#       - False -> file won't contain a header, first part is written to first line
#       - True -> file will have a header, if "header_text" is provided and not empty, then this text will be used instead of the property name
DOC = []
# Farnell
DOC.append({
    "distributor":"Farnell",
    "header":True,
    "header_text":["Part Number","Quantity","Description"],
    "properties":["ordNum","qnty","ref"],
    "delimiter":",",
    "delimiter_references":"/" # to separate multiple references inside the "ref"-cell
})
# Reichelt
DOC.append({
    "distributor":"Reichelt",
    "header":False,
    "header_text":None,
    "properties":["ordNum","qnty"],
    "delimiter":";",
    "delimiter_references":"/" # to separate multiple references inside the "ref"-cell
})
# Digikey
DOC.append({
    "distributor":"Digikey",
    "header":False,
    "header_text":None,
    "properties":["qnty","ordNum","ref"],
    "delimiter":",",
    "delimiter_references":"/" # to separate multiple references inside the "ref"-cell
})
# default
# NEEDS TO BE THE LAST ONE!
DOC.append({
    "distributor":"default",
    "header":True,
    "header_text":None,
    "properties":["qnty","ordNum","ref"],
    "delimiter":",",
    "delimiter_references":"/" # to separate multiple references inside the "ref"-cell
})

# summarized elementwise orderlist (SEO)
###################################################################################################
# list all properties, that each entry should contain (all properties except of "ref" used here has to be defined in PTI_REQ_PROPERTIES (see above))
SEO = ["Ref","manNum","distributor","ordNum","Package","value"]
SEO_HEADER = ["Reference","Manufacturer part name","Distributor","Order number","Package","Value"]
SEO_DELIMITER = "\t"

# additional attributes, user needs to organize his data
###################################################################################################
# attribut keys are strings, values have to be boolean -> checkbox
# value defined below in the attribute definition is the default value
# if the attribute value differs from the default value (user (un)checked corresponding checkbox),
# then the part will not be exported when generating the list of the ordering numbers
GUI_ITEM_ATTRIBUTES = {"ignore":False}