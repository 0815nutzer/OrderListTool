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

import copy
from enum import Enum, unique
import definitions as Definitions
import setup as Setup

class PartSource(Enum):
    DATABASE = 1
    BOM = 2

class Part():
    def __init__(self,part_type,args,source=None):
        self.properties = {}
        if not isinstance(args, dict):
            raise Exception("args is not a dictionary!")
        if not isinstance(part_type, str):
            raise Exception("part_type is not a string!")
        if source is None:
            raise Exception("define part source")
        if not isinstance(source,PartSource):
            raise Exception("source is not a PartSource")
        self.properties.update(args)
        self.part_type = part_type
        self.source = source

    def get_part_type(self):
        return self.part_type

    def set_part_type(self,part_type):
        if not isinstance(part_type,str):
            raise Exception("part_type is not an instance of string")
        self.part_type = copy.deepcopy(part_type)

    def get_property_value(self, key):
        if key in self.properties:
            return self.properties[key]
        return None

    def get_property_values(self, keys):
        properties=[]
        for k in keys:
            if k in self.properties:
                properties.append(self.properties[k])
            else:
                properties.append(None)
        return properties

    def set_property_values(self, properties):
        if isinstance(properties, list):
            for p in properties:
                if not isinstance(p, dict):
                    raise Exception("Wrong argument type, list elements of type dictionary expected!")
                self.properties.update(p)
        elif isinstance(properties, dict):
            self.properties.update(properties)
        else:
            raise Exception("Wrong argument type, dict or list of dicts expected!")

    def get_all_property_keys(self):
        return self.properties.keys()

    def get_all_property_values(self):
        return self.properties.values()

    def get_all_properties(self):
        return self.properties

    def is_equal(self,part,ignore_type=False,ignore_ref=True,pass_missing_property=False):
        if not isinstance(part,Part):
            raise Exception("part is not an instance of class Part")
        if not ignore_type:
            if self.part_type != part.get_part_type():
                return False
        part_properties = part.get_all_properties()
        if((
            any(prop not in part_properties for prop in self.properties) or
            any(prop not in self.properties for prop in part_properties)) and
            not pass_missing_property
        ):
            return False
        for prop in self.properties:
            if prop not in part_properties:
                continue
            if prop == "ref" and ignore_ref:
                continue
            # if self.properties[prop] != part_properties[prop]:
            if str(self.properties[prop]).replace(" ","") != str(part_properties[prop]).replace(" ",""):
                return False
        return True

@unique
class PartPropertyType(Enum):
    STRING = Definitions.DBKW_PART_PROPERTY_TYPE_STRING
    SUBSTRING = Definitions.DBKW_PART_PROPERTY_TYPE_SUBSTRING
    NUMBER_MAX = Definitions.DBKW_PART_PROPERTY_TYPE_NUMBER_MAX
    NUMBER_EQUAL = Definitions.DBKW_PART_PROPERTY_TYPE_NUMBER_EQUAL
    NUMBER_MIN = Definitions.DBKW_PART_PROPERTY_TYPE_NUMBER_MIN
    UNIT = Definitions.DBKW_PART_PROPERTY_TYPE_UNIT

class PartProperty():
    def __init__(self,name,property_type,default_value,symbol="",file="",src_text=""):
        if not isinstance(name,str):
            raise Exception("name is not a string")
        if not name:
            raise Exception("name has not to be empty")
        if not isinstance(property_type,PartPropertyType):
            raise Exception("property_type is not a string")
        if not property_type:
            raise Exception("property_type has not to be empty")
        if not isinstance(default_value,float) and not isinstance(default_value,str) and not default_value is None:
            raise Exception("default value has to be a float or a string")
        if not isinstance(symbol,str):
            raise Exception("symbol is not a string")
        self.name = name
        self.type = property_type
        self.symbol = symbol
        self.default_value = default_value
        self.file = file
        self.src_text = src_text

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_symbol(self):
        return self.symbol

    def get_default_value(self):
        return self.default_value

    def is_equal(self,compare):
        if not isinstance(compare,PartProperty):
            raise Exception("property to compare is not an instance of class PartProperty")
        if (
            self.name.replace(" ","") != compare.get_name().replace(" ","") or
            self.type != compare.get_type() or
            self.symbol.replace(" ","") != compare.get_symbol().replace(" ","") or
            str(self.default_value).replace(" ","") != str(compare.get_default_value()).replace(" ","")
        ):
            return False
        else:
            return True

    def get_file(self):
        return self.file

    def get_source_text(self):
        return self.src_text

class PartTemplate():
    def __init__(self,args):
        if not isinstance(args,dict):
            raise Exception("args is not a dictionary")
        if not isinstance(args["part_type"],str):
            raise Exception("template part_type is not a string")
        if not args["part_type"]:
            raise Exception("template part_type can not be empty")
        if not isinstance(args["reference_symbols"],list) and not args["reference_symbols"] is None:
            raise Exception("template reference_symbols is not a list")
        if not isinstance(args["keyword_database_file"],str) and not args["keyword_database_file"] is None:
            raise Exception("template keyword_database_file is not a string")
        if not args["keyword_database_file"] and not args["keyword_database_file"] is None:
            raise Exception("template keyword_database_file can not be empty")
        if args["part_type"].lower() == Definitions.BOMKW_PART_TYPE.lower():
            raise Exception("Cannot create part template of type " + args["part_type"] + "! Type is reserved for internal use!")
        if not isinstance(args["description"],str):
            raise Exception("template description is not a string")
        if any(requested not in args["requested_properties"] for requested in Setup.PTI_REQ_PROPERTIES):
            raise Exception("list requested_properties of template " + args["part_type"] + " does not contain all properties defined in PTI_REQ_PROPERTIES")
        self.part_type = args["part_type"]                              # part type. i.e. resistor, capacitor (see setup.py)
        self.properties = []                                            # properties of special part type, defined by partlist file
        self.requested_properties = args["requested_properties"]        # these are properties, that are necessary to receive a useful match
        self.reference_symbols = args["reference_symbols"]              # BOM symbols, that belongs to parts of this part type R -> resistor
        self.keyword_database_file = args["keyword_database_file"]      # a keyword, that has to be inside the part database filenames
        self.assigned_database_files = []                               # database files, containing part definitions belonging to this part type
        self.description = args["description"]                          # string describing the template type (for GUI)

    def get_description(self):
        return self.description

    def get_part_type(self):
        return self.part_type

    def get_reference_symbols(self):
        return self.reference_symbols

    def get_keyword_database_file(self):
        return self.keyword_database_file

    def assign_database_file(self,path):
        self.assigned_database_files.append(path)

    def get_assigned_database_files(self):
        return self.assigned_database_files

    def add_property(self,part_property):
        if not isinstance(part_property,PartProperty):
            raise Exception("part property is not an instance of PartProperty")
        self.properties.append(part_property)

    def contains_property(self,part_property):
        if not isinstance(part_property,PartProperty):
            raise Exception("part property is not an instance of PartProperty")
        for prop in self.properties:
            if part_property.get_name() == prop.get_name():
                return True
        return False

    def get_names_of_all_properties(self):
        names = []
        for prop in self.properties:
            names.append(prop.get_name())
        return names

    def get_names_of_requested_properties(self):
        return self.requested_properties

    def get_property(self,key):
        for prop in self.properties:
            if prop.get_name() == key:
                return prop
        return None

    def get_all_properties(self):
        return self.properties

    def value_to_string_or_float(self,key,value_str):
        for prop in self.properties:
            if prop.get_name() != key:
                continue
            if prop.get_type() == PartPropertyType.STRING or prop.get_type() == PartPropertyType.SUBSTRING or prop.get_type() == PartPropertyType.UNIT:
                return value_str
            else:
                return float(value_str.replace(" ",""))
        raise Exception("unknow template property: " + key + " in template: " + self.part_type)

    # use part template properties to create an empty part instance with predefined default property values
    def get_default_template_part_arguments(self):
        args = {}
        for prop in self.properties:
            args.update({prop.get_name():prop.get_default_value()})
            # if prop.get_type() == PartPropertyType.STRING:
            #     args.update({prop.get_name():""})
            # else:
            #     args.update({prop.get_name():None})
        return args

    def get_template_database_part(self):
        args = self.get_default_template_part_arguments()
        return Part(self.part_type,args,PartSource.DATABASE)

class Match():
    def __init__(self):
        self.bom_part = None
        self.matching_part = None

    def set_bom_part(self, part):
        if not isinstance(part, Part):
            raise Exception("part is not an instance of Part")
        if part.get_part_type() != Definitions.BOMKW_PART_TYPE:
            raise Exception("part is not a BOM part")
        self.bom_part = part

    def set_match(self, part):
        if not isinstance(part, Part):
            raise Exception("part is not an instance of Part")
        if part.get_part_type() == Definitions.BOMKW_PART_TYPE:
            raise Exception("BOM part could not be added as matching part!")
        self.matching_part = part

    def get_matching_part(self):
        return self.matching_part

    def get_bom_part(self):
        return self.bom_part

class Category():
    def __init__(self,template):
        if not isinstance(template,PartTemplate):
            raise Exception("template is not an instance of PartTemplate")
        self.part_template = template
        self.elements = []

    def get_part_type(self):
        return self.part_template.get_part_type()

    def get_reference_symbols(self):
        return self.part_template.get_reference_symbols()

    def get_part_template(self):
        return self.part_template

    def add_elements(self,elements):
        if isinstance(elements,list):
            self.elements.extend(elements)
            return
        else:
            self.elements.append(elements)

    def get_elements(self):
        return self.elements

    def get_number_of_elements(self):
        return len(self.elements)

    def clear(self):
        self.elements = []

class PartCategory(Category):
    def __init__(self,template):
        super().__init__(template)

    def add_parts(self,parts):
        if not isinstance(parts,Part) and not isinstance(parts,list):
            raise Exception("parts is neither an instance of Part nor of list")
        self.add_elements(parts)

class MatchCategory(Category):
    def __init__(self,template):
        super().__init__(template)

    def add_groups(self,groups):
        if not isinstance(groups,PartGroup) and not isinstance(groups,list):
            raise Exception("groups is neither an instance of PartGroup nor of list")
        self.add_elements(groups)

class PartGroup():
    def __init__(self,bom_part):
        if not isinstance(bom_part,Part):
            raise Exception("bom_part is not an instance of class Part")
        if bom_part.get_part_type() != Definitions.BOMKW_PART_TYPE:
            raise Exception("part is not a BOM part")
        self.bom_parts = [bom_part]
        self.matching_parts = []
        self.matches = []
        self.attributes = [copy.deepcopy(Setup.GUI_ITEM_ATTRIBUTES)]
        self.group_attributes = copy.deepcopy(Setup.GUI_ITEM_ATTRIBUTES)

    def add_bom_part(self,bom_part):
        if not isinstance(bom_part,Part):
            raise Exception("bom_part is not an instance of class Part")
        if bom_part.get_part_type() != Definitions.BOMKW_PART_TYPE:
            raise Exception("part is not a BOM part")
        self.bom_parts.append(bom_part)
        self.attributes.extend([copy.deepcopy(Setup.GUI_ITEM_ATTRIBUTES)])

    def add_matching_part(self,matching_part):
        if not isinstance(matching_part,Part):
            raise Exception("matching_part is not an instance of class Part")
        if matching_part.get_part_type() == Definitions.BOMKW_PART_TYPE:
            raise Exception("part is a BOM part")
        self.matching_parts.append(matching_part)

    def add_match(self,match):
        if not isinstance(match,Match):
            raise Exception("match is not an instance of class Match")
        self.matches.append(match)

    def get_reference_bom_part(self):
        return self.bom_parts[0]

    def get_bom_parts(self):
        return self.bom_parts

    def get_matching_parts(self):
        return self.matching_parts

    def get_matching_part_index(self,index):
        if not isinstance(index,int):
            raise Exception("index has to be an integer")
        if index >= len(self.matching_parts) or index < 0:
            raise Exception("index out of bounds")
        return self.matching_parts[index]

    def get_number_of_bom_parts(self):
        return len(self.bom_parts)

    def get_number_of_matching_parts(self):
        return len(self.matching_parts)

    def get_number_of_attributes(self):
        return len(self.attributes)

    def get_matches(self):
        return self.matches

    def get_match(self,index):
        if not isinstance(index,int):
            raise Exception("index has to be an integer")
        if index >= len(self.matches) or index < 0:
            raise Exception("index out of bounds")
        return self.matches[index]

    def get_attributes(self,index=None):
        if index is None:
            return self.attributes
        else:
            if not isinstance(index,int):
                raise Exception("index has to be an integer")
            return self.attributes[index]

    def set_attributes(self,attributes,index=None):
        if index is None:
            if not isinstance(attributes,list):
                raise Exception("attributes is not a list")
            if len(self.attributes) != len(attributes):
                raise Exception("different length of attribute list")
            self.attributes = attributes
        else:
            if not isinstance(index,int):
                raise Exception("index has to be an integer")
            if not isinstance(attributes,dict):
                raise Exception("attributes is not a dictionary")
            return self.attributes[index].update(attributes)

    def get_group_attributes(self):
        self.determine_group_attributes()
        return self.group_attributes

    def get_deviating_group_attributes(self):
        result = {}
        for group_attribute in self.group_attributes:
            for attributes in self.attributes:
                if self.group_attributes[group_attribute] != attributes[group_attribute]:
                    result.update({group_attribute:True})
                    break
            else:
                result.update({group_attribute:False})
        return result

    def determine_group_attributes(self):
        for attribute in self.group_attributes:
            for match_attributes in self.attributes:
                if match_attributes[attribute] == Setup.GUI_ITEM_ATTRIBUTES[attribute]:
                    self.group_attributes[attribute] = Setup.GUI_ITEM_ATTRIBUTES[attribute]
                    break
            else:
                self.group_attributes[attribute] = not Setup.GUI_ITEM_ATTRIBUTES[attribute]

class OrderListItem():
    def __init__(self,match,ignore=False):
        if not isinstance(match,Match):
            raise Exception("match is not an instance of class Match")
        if not isinstance(ignore,bool):
            raise Exception("ignore is not a boolean")
        self.properties = copy.deepcopy(match.get_bom_part().get_all_properties())
        # doing this, will override properties always got from BOM part (i.e. value)
        self.properties.update(copy.deepcopy(match.get_matching_part().get_all_properties()))
        self.ignore = ignore

    def is_ignored(self):
        return self.ignore

    def get_properties(self):
        return self.properties

    def get_property_values(self,keys):
        if isinstance(keys,list):
            values = {}
            for key in keys:
                if key not in self.properties:
                    values.update({key:None})
                else:
                    values.update({key:self.properties[key]})
            return values
        else:
            if not isinstance(keys,str):
                raise Exception("keys is neither a string nor a list")
            if keys not in self.properties:
                return None
            else:
                return self.properties[keys]

    def is_equal(self,item,ignore_ref=True):
        if not isinstance(item,OrderListItem):
            raise Exception("item is not an instance of class OrderListItem")
        item_properties = item.get_properties()
        if any(prop not in item_properties for prop in self.properties):
            return False
        if any(prop not in self.properties for prop in item_properties):
            return False
        for prop in self.properties:
            if prop == "ref" and ignore_ref:
                continue
            if str(self.properties[prop]).replace(" ","") != str(item_properties[prop]).replace(" ",""):
                return False
        return True

    def get_list_item_string(self,properties):
        return Setup.SEO_DELIMITER.join([self.properties[prop.lower()] for prop in properties])

class OrderListGroup():
    def __init__(self,item):
        if not isinstance(item,OrderListItem):
            raise Exception("item is not an instance of class OrderListItem")
        self.items = []
        self.items.append(item)

    def add_item(self,item):
        if not isinstance(item,OrderListItem):
            raise Exception("item is not an instance of class OrderListItem")
        self.items.append(item)

    def get_reference_item(self):
        return self.items[0]

    def get_quantity(self):
        return len(self.items)

    def get_distributor(self):
        return self.items[0].get_property_values("distributor")

    def add_order_list_properties(self,distributor,lst):
        if not isinstance(distributor,OrderListDristributor):
            raise Exception("distributor is not an instance of OrderListDistributor")
        if not isinstance(lst,list):
            raise Exception("lst is not an instance of list")
        # get properties of database parts
        properties = copy.deepcopy(self.items[0].get_property_values(distributor.get_property_order()))
        # add quantity value
        properties.update({"qnty":len(self.items)})
        # override ref-property
        ref = distributor.get_delimiter_references().join([item.get_property_values("ref") for item in self.items])
        properties.update({"ref":ref})
        # check, if ordNum contains multiple entrys
        ord_numbers = properties["ordnum"].split(Definitions.DBKW_SEPARATOR_ORDNUM)
        if len(ord_numbers) <= 1:
            # only one part to order
            lst.append([properties[prop] for prop in distributor.get_property_order()])
        else:
            # multiple parts to order
            for ord_number in ord_numbers:
                properties.update({"ordnum":ord_number.lstrip().rstrip()})
                lst.append([properties[prop] for prop in distributor.get_property_order()])

class OrderListDristributor():
    def __init__(self,args):
        if not isinstance(args, dict):
            raise Exception("args is not a dictionary!")
        try:
            self.distributor = args["distributor"]
            self.header = args["header"]
            self.header_text = args["header_text"]
            self.properties = [prop.lower() for prop in args["properties"]]
            self.delimiter = args["delimiter"]
            self.delimiter_references = args["delimiter_references"]
        except Exception as e:
            raise Exception("error while evaluating distributor orderlist configuration. Check definitions! Error: " + e.args[0]) from e
        self.groups = []

    def get_distributor(self):
        return self.distributor

    def get_delimiter(self):
        return self.delimiter

    def get_delimiter_references(self):
        return self.delimiter_references

    def get_property_order(self):
        return self.properties

    def add_group(self,group):
        if not isinstance(group,OrderListGroup):
            raise Exception("group is not an instance of class OrderListGroup")
        self.groups.append(group)

    def write_file(self,file):
        # if there are no order list groups, then there is nothing to do
        if len(self.groups) <= 0:
            return
        # collect all lines
        lines = []
        prop_per_item = []
        for group in self.groups:
            group.add_order_list_properties(self,prop_per_item)
        # if properties "ordnum" and "qnty" are present, then it is possible to summarize equal ordering numbers
        # otherwise not
        if any(prop not in self.properties for prop in ["ordnum", "qnty"]):
            # not able to summarize
            for item_properties in prop_per_item:
                lines.append(self.delimiter.join([str(item) for item in item_properties]))
        else:
            # summarizing is possible
            # ordnum is keept
            # qnty is added
            # ref is concatenated
            # others is taken from first entry
            summarized = []
            index_ordnum = self.properties.index("ordnum")
            index_qnty = self.properties.index("qnty")
            if "ref" in self.properties:
                index_ref = self.properties.index("ref")
            else:
                index_ref = None
            for item_properties in prop_per_item:
                for item_summarized in summarized:
                    if item_summarized[index_ordnum] == item_properties[index_ordnum]:
                        item_summarized[index_qnty] += item_properties[index_qnty]
                        if index_ref is not None:
                            item_summarized[index_ref] = self.delimiter_references.join([item_summarized[index_ref], item_properties[index_ref]])
                        break
                else:
                    summarized.append(item_properties)
            # create lines
            for item_summarized in summarized:
                lines.append(self.delimiter.join([str(item) for item in item_summarized]))
        try:
            fobj = open(file,"w")
            # write header if requested
            if self.header and self.header_text is not None:
                fobj.write(self.delimiter.join(self.header_text))
                fobj.write("\n")
            # write each order list group into one line
            fobj.write("\n".join(lines))
            # done, so close file
            fobj.close()
        except Exception as e:
            raise Exception("failed writing output to file: " + file + " Error: " + e.args[0]) from e
