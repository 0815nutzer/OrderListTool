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
import os
import definitions as Definitions
import settings as Settings
import parts as Parts

def parse_file_for_part_template_properties(file,template):
    if not os.path.isfile(file):
        raise Exception(file + " is not a file")
    if not isinstance(template,Parts.PartTemplate):
        raise Exception("template is not an instance of PartTemplate")

    # read in file
    try:
        fobj = open(file)
        lines = fobj.readlines()
        # close file
        fobj.close()
    except IOError:
        raise Exception("could not open file: " + file) from IOError

    # search section, where properties are defined
    prop_start = 0
    for line in lines:
        prop_start += 1      # points to line below the searched keyword
        line = line.rstrip('\n\r').lstrip()
        if line.startswith(Definitions.DBKW_COMMENT):
            continue
        if line == Definitions.DBKW_DEFINE_PROPERTIES:
            break

    # section found? if not, then return
    if prop_start >= len(lines):
        raise Exception("no " + Definitions.DBKW_DEFINE_PROPERTIES + " section found in file: " + file)

    # read properties until end of definition
    properties = []
    for line in lines[prop_start:]:
        line = line.rstrip('\n\r').lstrip()
        # skip comment line
        if line.startswith(Definitions.DBKW_COMMENT):
            continue
        # skip database file entry properties definition
        if Definitions.DBKW_SEPARATOR_ELEMENT in line:
            continue
        # end of section reached -> break
        if line == Definitions.DBKW_DEFINE_END:
            break
        properties.append(line)
    # we reached end of file without occurence of ENDDEFINITION
    else:
        raise Exception("no " + Definitions.DBKW_DEFINE_END + " found for properties section in file: " + file )

    instances = []
    instance_names = []
    # convert text into PartProperty object
    for prop in properties:
        split = prop.split(Definitions.DBKW_SEPARATOR_PROPERTY)
        if len(split) != 2 and len(split) != 4:
            raise Exception("wrong property definition: " + prop + " in file: " + file)
        try:
            if len(split) == 4:
                if any(sub == "" for sub in split):
                    raise Exception("wrong property definition: " + prop + " in file: " + file)
                symbol = split[2]
                # default value as number or String
                if split[1].lower() == Parts.PartPropertyType.STRING.value.lower() or split[1].lower() == Parts.PartPropertyType.SUBSTRING.value.lower():
                    default_value = split[3]
                else:
                    default_value = float(split[3])
            else:
                symbol = ""
                default_value = None
            part_property = Parts.PartProperty(split[0].lower(),Parts.PartPropertyType(split[1]),default_value,symbol,file,prop)
        except Exception as e:
            raise Exception("could not create part property instance from property definition: " + prop + " Check definition!") from e
        instances.append(part_property)
        instance_names.append(part_property.get_name())
    # check, if file contains all required instances
    if any(name.lower() not in instance_names for name in template.get_names_of_requested_properties()):
        raise Exception("File " + file + " does not contain property definitions for all requested properties of this part type.")
    # check if there already exists this property -> then do not add it again
    for instance in instances:
        if template.contains_property(instance):
            # if property definitions differ, raise an error
            if not template.get_property(instance.get_name()).is_equal(instance):
                raise Exception('property "' + instance.get_name() +
                    '" already defined in different way ' + instance.get_source_text() +
                    " in file " + instance.get_file())
            continue
        template.add_property(instance)
    # 

def get_part_template_properties(template):
    for element in template.get_assigned_database_files():
        parse_file_for_part_template_properties(element,template)

def parse_file_for_parts(file,template):
    if not os.path.isfile(file):
        raise Exception(file + " is not a file")
    if not isinstance(template,Parts.PartTemplate):
        raise Exception("template is not an instance of PartTemplate")

    parts = []

    # read in file
    try:
        fobj = open(file)
        lines = fobj.readlines()
        # close file
        fobj.close()
    except IOError:
        raise Exception("could not open file: " + file) from IOError

    # search section, where properties are defined
    prop_start = 0
    for line in lines:
        prop_start += 1      # points to line below the searched keyword
        line = line.rstrip('\n\r').lstrip()
        if line.startswith(Definitions.DBKW_COMMENT):
            continue
        if line == Definitions.DBKW_DEFINE_PROPERTIES:
            break

    # section found? if not, then return
    if prop_start >= len(lines):
        raise Exception("no " + Definitions.DBKW_DEFINE_PROPERTIES + " section found in file: " + file)

    # search end of section
    prop_end = prop_start
    for line in lines[prop_start:]:
        prop_end += 1 # points to line below searched keyword
        line = line.rstrip('\n\r').lstrip()
        # skip comment
        if line.startswith(Definitions.DBKW_COMMENT):
            continue
        # prperty order of database file entry
        if Definitions.DBKW_SEPARATOR_ELEMENT in line:
            file_entry_property_order = line.lower().split(Definitions.DBKW_SEPARATOR_ELEMENT)
            continue
        # end of section reached -> break
        if line == Definitions.DBKW_DEFINE_END:
            break
    # we reached end of file without occurence of ENDDEFINITION
    else:
        raise Exception("no " + Definitions.DBKW_DEFINE_END + " found for properties section in file: " + file )

    # prepare the obtained file entry property order for later use
    for prop_name in file_entry_property_order:
        prop = template.get_property(prop_name)
        if prop is None:
            raise Exception("property " + prop_name + " used in property definition section is not defined. file: " + file)

    # remove property definition section from input
    del lines[prop_start-1:prop_end]
    # data = [line.rstrip("\n\r").lstrip().replace(" ","") for line in lines
    data = [line.rstrip("\n\r").lstrip() for line in lines
        if not line.startswith(Definitions.DBKW_COMMENT)
        and not line.startswith("\n")
        and not line.startswith("\r")
        and (Definitions.DBKW_SEPARATOR_PROPERTY in line or Definitions.DBKW_SEPARATOR_ELEMENT in line)]

    # template part
    template_part = template.get_template_database_part()
    template_part_properties = template.get_names_of_all_properties()

    # parse data
    for entry in data:
        # line with colon -> set property
        if Definitions.DBKW_SEPARATOR_PROPERTY in entry:
            # split string into property name and property value
            sep = entry.split(Definitions.DBKW_SEPARATOR_PROPERTY)
            sep[0] = sep[0].lower()
            if len(sep) != 2 or any(sub == "" for sub in sep):
                raise Exception("wrong property definition: " + entry + " in file: " + file)
            if sep[0] not in template_part_properties:
                raise Exception("requested property not defined! " + entry + " in file: " + file)
            # check, if property value is a string or a number
            key = sep[0]
            value = template.value_to_string_or_float(key,sep[1])
            template_part.set_property_values({key:value})
        # line with semicolon -> element
        elif Definitions.DBKW_SEPARATOR_ELEMENT in entry:
            # split string into elements
            sep = entry.split(Definitions.DBKW_SEPARATOR_ELEMENT)
            if any(sub == "" for sub in sep) or len(sep) != len(file_entry_property_order):
                raise Exception("Wrong element definition! Expected: " + file_entry_property_order + " Found: " + entry + " in file: " + file)
            # convert value
            for i in range(0,len(file_entry_property_order)):
                template_part.set_property_values({file_entry_property_order[i]:template.value_to_string_or_float(file_entry_property_order[i],sep[i])})
            parts.append(copy.deepcopy(template_part))    
    return parts
    
def read_database(template):
    parts = []
    for element in template.get_assigned_database_files():
        parts.extend(parse_file_for_parts(element,template))
    return parts

def read_bom_file(file,dispatcher):
    properties = []
    parts = []

    # open file
    try:
        fobj = open(file)
        lines=fobj.readlines()
        # close file
        fobj.close()
    except IOError:
        raise Exception ("could not open BOM file: " + file) from IOError

    # search section, where properties are defined
    prop_start = 0
    for line in lines:
        prop_start += 1      # points to line below the searched keyword
        line=line.rstrip('\n\r').lstrip().replace('"','')
        if line.startswith(Definitions.BOMKW_COMMENT):
            continue
        if line == Definitions.BOMKW_DEFINE_PROPERTIES:
            break

    # section found? if not, then return
    if prop_start >= len(lines):
        raise Exception("no " + Definitions.BOMKW_DEFINE_PROPERTIES + " section found in BOM file: " + file)

    # read properties until end of definition
    for line in lines[prop_start:]:
        line=line.rstrip('\n\r').lstrip().replace('"','')
        if line.startswith(Definitions.BOMKW_COMMENT):
            continue
        if line == Definitions.BOMKW_DEFINE_END:
            break
        # get all properties in line
        properties.extend(line.lower().split(Definitions.BOMKW_DELIMITER))
    # we reached end of file without occurence of ENDDEFINITION
    else:
        raise Exception("no " + Definitions.BOMKW_DEFINE_END + " found for properties section in BOM file: " + file )

    # check if all requested properties are present
    if any(p.lower() not in properties for p in dispatcher.get_cad_system().get_req_bom_part_properties()):
        raise Exception("BOM file does not contain all requested properties: " + file)

    # build part template using obtained properties
    template = dict(list(zip(properties, [0]*len(properties))))

    # search section, where parts are listed
    data_start = 0
    for line in lines:
        data_start += 1      # points to line below the searched keyword
        line=line.rstrip('\n\r').lstrip().replace('"','')
        if line.startswith(Definitions.BOMKW_COMMENT):
            continue
        if line == Definitions.BOMKW_DEFINE_DATA:
            break

    # section found? if not, then return
    if data_start >= len(lines):
        raise Exception("no " + Definitions.BOMKW_DEFINE_DATA + " section found in BOM file: " + file)

    # get mapping of keywords
    req_bom_part_properties = dispatcher.get_cad_system().get_req_bom_part_properties()
    if len(Definitions.BOMKW_PART_PROPERTIES) != len(req_bom_part_properties):
        raise Exception("length of BOM part property mapping differs! Check Definitions! " +  Definitions.BOMKW_PART_PROPERTIES + " vs. " + req_bom_part_properties)
    mapped_keywords = {}
    for i in range(len(Definitions.BOMKW_PART_PROPERTIES)):
        mapped_keywords.update({Definitions.BOMKW_PART_PROPERTIES[i]:req_bom_part_properties[i]})

    # now parse file line by line
    n = data_start
    for line in lines[data_start:]:
        n += 1
        line=line.rstrip('\n\r').lstrip().replace('"','').replace(' ','')
        # skip comments
        if line.startswith(Definitions.BOMKW_COMMENT):
            continue
        if line == Definitions.BOMKW_DEFINE_END:
            break
        # split string into elements
        sep = line.split(Definitions.BOMKW_DELIMITER)
        if (len(sep) ) != len(properties):
            raise Exception("wrong element definition at line " + str(n) + " in BOM file: " + file)
        # assign values to properties
        for p in range(0,len(properties)):
            if properties[p] in template:
                template[properties[p]]=sep[p]
        # get ref-string
        refs = template[mapped_keywords["ref"]].split(Definitions.BOMKW_SEPARATOR_ELEMENT)
        for r in refs:
            # remove reference digits and compare to ignore reference symbols
            if any(ref == ''.join(i for i in r if not i.isdigit()) for ref in dispatcher.get_cad_system().get_ignored_ref_symbols()):
                continue
            template[mapped_keywords["ref"]]=r
            parts.append(copy.deepcopy(template))
    # we reached end of file without occurence of ENDDEFINITION
    else:
        raise Exception("no " + Definitions.BOMKW_DEFINE_END + " found for data section in BOM file: " + file )

    # map part properties to requested properties and create part instance
    # i.e. KiCAD uses "footprint" but here we need "package" -> see global file
    template = Parts.Part(
        Definitions.BOMKW_PART_TYPE,
        dict(list(zip(Definitions.BOMKW_PART_PROPERTIES, [0]*len(Definitions.BOMKW_PART_PROPERTIES)))),
        Parts.PartSource.BOM
    )
    mapped_parts = []
    for part in parts:
        args = {}
        bom_req_properties = dispatcher.get_cad_system().get_req_bom_part_properties()
        for i in range(0,len(Definitions.BOMKW_PART_PROPERTIES)):
            args.update({Definitions.BOMKW_PART_PROPERTIES[i]:part[bom_req_properties[i]]})
        template.set_property_values(args)
        mapped_parts.append(copy.deepcopy(template))

    return mapped_parts

def property_string_to_value(string,value_type,symbol=None):
    if not isinstance(string, str):
        raise Exception("argument string is not a string")
    if not isinstance(value_type,Parts.PartPropertyType):
        raise Exception("value_type is not an instance of PartPropertyType")
    if symbol is None:
        # no symbol to remove
        cropped = string
    else:
        if not isinstance(symbol,str):
            raise Exception("argument symbol is not a string")
        # if string ends with symbol, then only remove it
        if string.endswith(symbol):
            cropped = string.replace(symbol,"")
        else:
            # symbol is inside string, replace it by a dot
            cropped = string.replace(symbol,"")
    try:
        if value_type == Parts.PartPropertyType.STRING or value_type == Parts.PartPropertyType.SUBSTRING:
            return cropped
        else:
            return float(cropped)
    except Exception as e:
        raise Exception("failed to convert string: " + string + " into value: " + e.args[0]) from e

def compare_value_strings_if_equal(values):
    if not isinstance(values,list):
        raise Exception("values is not a list")
    if len(values) < 2:
        raise Exception("values must have at least two elements")
    unit_prefixes = Definitions.UNIT_PREFIX.keys()
    valid_chars = "0123456789." + "".join(list(unit_prefixes))
    # norm values
    values_normed = []
    for value in values:
        if not isinstance(value,str):
            raise Exception("at least one value inside values is not a string")
        if not value:
            # raise Exception("value is empty")
            return False
        # replace everything, that is not a unit prefix or a digit or a dot by ~
        value = "".join([char for char in value if char in valid_chars])
        # determine unit symbol
        for prefix in unit_prefixes:
            if prefix in value:
                break
        else:
            prefix = "~"
        # replace unit prefix by space, if there is already a dot inside the value string or if the value string ends with unit prefix
        # otherwise replace unit prefix by dot
        # constraint: if value string contains a dot, than the value string must not contain any digit after unit prefix
        # 1k8 -> 1.8
        # 18k -> 18
        # 0.01u -> 0.01
        if "." in value or value.endswith(prefix):
            value = value.replace(prefix,"")
        else:
            value = value.replace(prefix,".")
        # if not able to convert number, then values are not compareable
        try:
            number = float(value)
        except Exception:
            return False
        if number != 0:
            while number < 1 or number > 1000:
                current_exponent = Definitions.UNIT_PREFIX[prefix]["exp"]
                if number < 1:
                    prefix = Definitions.UNIT_PREFIX[prefix]["smaller"]
                elif number > 1000:
                    prefix = Definitions.UNIT_PREFIX[prefix]["bigger"]
                new_exponent = Definitions.UNIT_PREFIX[prefix]["exp"]
                # multiply number with difference in exponents
                number *= (10**(current_exponent - new_exponent))
        # now the value is between 1 and 1000, and prefix is manipulated also
        values_normed.append(str(number) + "e" + str(Definitions.UNIT_PREFIX[prefix]["exp"]))
    # now compare, if all normed values are equal
    for element in values_normed[:-1]:
        if element != values_normed[-1]:
            return False
    return True
