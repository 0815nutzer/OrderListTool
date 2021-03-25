import settings as Settings

# keywords in part database files (DBKW_)
DBKW_DATABASEFILE = "partlist"
DBKW_COMMENT = "#"
DBKW_DEFINE_END = "ENDDEFINE"
DBKW_DEFINE_PROPERTIES = "DEFINE_PROPERTIES"
DBKW_PROPERTY_PACKAGE = "PACKAGE"
DBKW_SEPARATOR_PROPERTY = ":"
DBKW_SEPARATOR_ELEMENT = ";"
DBKW_SEPARATOR_ORDNUM = "&"

# define property type strings used in database files
DBKW_PART_PROPERTY_TYPE_STRING = "STRING"
DBKW_PART_PROPERTY_TYPE_SUBSTRING = "SUBSTRING"
DBKW_PART_PROPERTY_TYPE_NUMBER_MAX = "NUMBER_MAX"
DBKW_PART_PROPERTY_TYPE_NUMBER_EQUAL = "NUMBER_EQUAL"
DBKW_PART_PROPERTY_TYPE_NUMBER_MIN = "NUMBER_MIN"
DBKW_PART_PROPERTY_TYPE_UNIT = "UNIT"

# keywords in BOM file (BOMKW_)
BOMKW_COMMENT = "#"
BOMKW_DEFINE_END = "ENDDEFINE"
BOMKW_DEFINE_PROPERTIES = "DEFINE_PROPERTIES"
BOMKW_DEFINE_DATA = "DEFINE_DATA"
BOMKW_DELIMITER = ";"
BOMKW_SEPARATOR_ELEMENT = ","
BOMKW_SEPARATOR_VALUE = "/"

# order of BOMKW_PART_PROPERTIES has to be equal to order of BOMKW_REQ_PROPERTIES!
BOMKW_PART_PROPERTIES = ["ref", "value", "package"]
BOMKW_PART_TYPE = "BOM"
BOMKW_REQ_PROPERTIES = Settings.BOMKW_REQ_PROPERTIES

# GUI settings
GUI_WIDTH_BUTTON = 150
GUI_HEIGHT_BUTTON = 40
GUI_HEIGHT_ITEM = 30
GUI_WIDTH_ITEM_REF = 150
GUI_WIDTH_ITEM_VALUE = 150
GUI_WIDTH_ITEM_PACKAGE = 300
GUI_WIDTH_ITEM_QNTY = 30
GUI_WIDTH_ITEM_OTHERS = 120
GUI_WIDTH_ITEM_CHECKBOX = 20
GUI_HEIGHT_ITEM_CHECKBOX = 15

# unit prefixes
UNIT_PREFIX = {
    "E":{
        "exp":18,
        "bigger":"X",
        "smaller":"P"
    },
    "P":{
        "exp":15,
        "bigger":"E",
        "smaller":"T"
    },
    "T":{
        "exp":12,
        "bigger":"P",
        "smaller":"G"
    },
    "G":{
        "exp":9,
        "bigger":"T",
        "smaller":"M"
    },
    "Meg":{
        "exp":6,
        "bigger":"G",
        "smaller":"k"
    },
    "M":{
        "exp":6,
        "bigger":"G",
        "smaller":"k"
    },
    "k":{
        "exp":3,
        "bigger":"M",
        "smaller":"~"
    },
    "h":{
        "exp":2,
        "bigger":"k",
        "smaller":"~"
    },
    "da":{
        "exp":1,
        "bigger":"k",
        "smaller":"~"
    },
    "~":{
        "exp":0,
        "bigger":"k",
        "smaller":"m"
    },
    "d":{
        "exp":-1,
        "bigger":"~",
        "smaller":"m"
    },
    "c":{
        "exp":-2,
        "bigger":"~",
        "smaller":"m"
    },
    "m":{
        "exp":-3,
        "bigger":"~",
        "smaller":"u"
    },
    "µ":{
        "exp":-6,
        "bigger":"m",
        "smaller":"n"
    },
    "u":{
        "exp":-6,
        "bigger":"m",
        "smaller":"n"
    },
    "n":{
        "exp":-9,
        "bigger":"u",
        "smaller":"p"
    },
    "p":{
        "exp":-12,
        "bigger":"n",
        "smaller":"f"
    },
    "f":{
        "exp":-15,
        "bigger":"p",
        "smaller":"a"
    },
    "a":{
        "exp":-18,
        "bigger":"f",
        "smaller":"x"
    },
}
