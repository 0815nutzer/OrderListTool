# default settings
DEFAULT_SYSTEM = "KiCAD"
DEFAULT_DIRECTORY = ""
DEFAULT_FILE = ""
LANGUAGE = "de"     # en, de

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
