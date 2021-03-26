# imports
import os
import copy
import definitions as Definitions
import settings as Settings
import setup as Setup
import parts as Parts
import visualization as Visualization
import parseFunctions as pF

# manages the requests from GUI
class Dispatcher():
    def __init__(self):
        # local variables
        self.bom_file_path = None
        self.database_path = None
        self.bom_parts = []
        self.bom_part_groups = []
        self.database_part_categories = []
        self.match_categories = []
        self.part_templates = []
        self.assigned_reference_symbols = []
        self.assigned_database_file_keywords = []
        self.order_list_items = []
        self.order_list_groups = []
        self.order_list_distributors = []
        # get system depending settings
        self.cad_system = System()

    def get_cad_system(self):
        return self.cad_system

    def set_bom_file_path(self,path):
        if not isinstance(path,str):
            raise Exception("BOM file path is not a string")
        if not path:
            raise Exception("BOM file path is empty")
        self.bom_file_path = path

    def set_database_path(self,path):
        if not isinstance(path,str):
            raise Exception("path for database files is not a string")
        if not path:
            raise Exception("path for database files is empty")
        self.database_path = path

    def create_part_templates(self):
        self.part_templates = []
        self.assigned_reference_symbols = []
        self.assigned_database_file_keywords = []
        for element in Setup.PTI:
            template = Parts.PartTemplate(element)
            if template.get_keyword_database_file() in self.assigned_database_file_keywords:
                raise Exception("keyword assigned twice: " + template.get_keyword_database_file())
            if not template.get_reference_symbols():
                raise Exception("there are no reference symbols defined for template: " + template.get_part_type())
            for symbol in template.get_reference_symbols():
                if symbol in self.assigned_reference_symbols:
                    raise Exception("reference symbol assigned twice: " + symbol)
            self.assigned_reference_symbols.extend(template.get_reference_symbols())
            self.assigned_database_file_keywords.append(template.get_keyword_database_file())
            self.part_templates.append(template)
        # add an additional part template for all parts, not belonging to user defined part templates
        args = {
            "part_type":"others",
            "requested_properties":copy.deepcopy(Setup.PTI_REQ_PROPERTIES),
            "reference_symbols":None,
            "keyword_database_file":None,
            "description":"weitere Bauteile"
        }
        self.part_templates.append(Parts.PartTemplate(args))

    def assign_database_files_to_templates(self):
        if self.database_path is None:
            raise Exception("path of database files not set")
        # get all files in this folder
        files = [f for f in os.listdir(self.database_path) if os.path.isfile(os.path.join(self.database_path, f))]
        # remove all files, that do not contain "partlist" within file name
        for f in files:
            if Definitions.DBKW_DATABASEFILE not in f.lower():
                files.remove(f)
        # assign file to corresponding part template
        for f in files:
            for template in self.part_templates:
                # no database file keyword defined
                if template.get_keyword_database_file() is None:
                    continue
                # if file name contains template keyword, then assign it to template
                if template.get_keyword_database_file() in f.lower():
                    template.assign_database_file(os.path.join(self.database_path, f))
                    break
            # no match found -> assign it to others
            else:
                self.part_templates[-1].assign_database_file(os.path.join(self.database_path, f))

    def get_part_template_properties(self):
        for template in self.part_templates:
            pF.get_part_template_properties(template)

    def read_database(self):
        self.database_part_categories = []
        if self.database_path is None:
            raise Exception("path of database files not set")
        # each template will result in it's own category
        for template in self.part_templates:
            category = Parts.PartCategory(template)
            category.add_parts(pF.read_database(template))
            self.database_part_categories.append(category)

    def read_bom_file(self):
        self.bom_parts = []
        if self.bom_file_path is None:
            raise Exception("path of BOM file not set")
        self.bom_parts.extend(pF.read_bom_file(self.bom_file_path,self))

    def group_bom_parts(self):
        self.bom_part_groups = []
        # check for each BOM part, if it is equal to another one (except of reference symbol)
        # if, then add it to this group, if not then create a new group
        for bom_part in self.bom_parts:
            for group in self.bom_part_groups:
                if bom_part.is_equal(group.get_reference_bom_part()):
                    group.add_bom_part(bom_part)
                    break
            else:
                # no match -> new group
                self.bom_part_groups.append(Parts.PartGroup(bom_part))

    def regroup_parts(self):
        part_groups = []
        # category wise
        for category in self.match_categories:
            category_groups = []
            # for each category group
            for group in category.get_elements():
                matches = group.get_matches()
                # for each match (BOM part and selected counterpart) in this group
                for i in range(len(matches)):
                    match = matches[i]
                    # compare to each new group
                    for part_group in part_groups:
                        # compare BOM part
                        if not match.get_bom_part().is_equal(part_group.get_reference_bom_part()):
                            continue
                        if match.get_matching_part() != part_group.get_match(0).get_matching_part():
                            continue
                        # BOM part of current match is equal to group reference BOM part and
                        # the same matching part is selected
                        # so add BOM part and match to this group
                        part_group.add_bom_part(match.get_bom_part())
                        part_group.add_match(match)
                        part_group.set_attributes(group.get_attributes(i),-1)
                        break
                    # no match, create new group
                    else:
                        # new group based on current BOM part
                        new_group = Parts.PartGroup(match.get_bom_part())
                        # add this match
                        new_group.add_match(match)
                        # copy attributes
                        new_group.set_attributes(group.get_attributes(i),0)
                        # add matching parts
                        for matching_part in group.get_matching_parts():
                            new_group.add_matching_part(matching_part)
                        # add this group to arrays
                        part_groups.append(new_group)
                        category_groups.append(new_group)
            # replace old group structure by new one
            category.clear()
            category.add_groups(category_groups)
        # replace old bom part groups by new one
        self.bom_part_groups = part_groups

    def find_matches(self):
        self.match_categories = []
        # need to do some stuff before
        try:
            # prepare database
            self.create_part_templates()
            self.assign_database_files_to_templates()
            self.get_part_template_properties()
            self.read_database()
            # read BOM file and group equal bom parts
            self.read_bom_file()
            self.group_bom_parts()
        except Exception as e:
            raise Exception("failed to read database or BOM file: " + e.args[0]) from e
        # check, if something was found
        if len(self.database_part_categories) <= 0:
            raise Exception("No database parts found. Database is empty!")
        if len(self.bom_parts) <= 0:
            raise Exception("No BOM parts found in BOM part file. BOM is empty!")

        # iterate through all categories and search for BOM parts with same reference
        for database_category in self.database_part_categories:
            match_category = Parts.MatchCategory(database_category.get_part_template())
            property_symbols = []
            database_properties = database_category.get_part_template().get_all_properties()
            # collect symbols of category template properties
            for prop in database_properties:
                symbol = prop.get_symbol().replace(" ","")
                if symbol is None or not symbol:
                    continue
                property_symbols.append(prop.get_symbol())
            # iterate BOM part groups
            for bom_part_group in self.bom_part_groups:
                bom_part = bom_part_group.get_reference_bom_part()
                bom_part_properties = copy.deepcopy(bom_part.get_all_properties())
                # comparison of reference symbols depends on database_category:
                #   if database_category is the default category, then the BOM reference should not be one of the assigned category references
                #   if database_category is not the default category, then one of the category reference symbols has to be equal to the BOM part reference
                # remove all digits from BOM part reference
                reference_cropped = "".join([char for char in bom_part_properties["ref"].replace(" ","") if char not in "0123456789"])
                if database_category.get_reference_symbols() is None:
                    # default category
                    # reference symbol match -> next part
                    if any(reference == reference_cropped for reference in self.assigned_reference_symbols):
                        continue
                else:
                    # not default category
                    # no reference symbol match -> next part
                    if not any(reference == reference_cropped for reference in database_category.get_reference_symbols()):
                        continue
                # add all category properties to BOM part in this group and investigate BOM part value
                default_part_properties = database_category.get_part_template().get_template_database_part().get_all_properties()
                bom_part_properties.update({key:default_part_properties[key] for key in default_part_properties if key not in bom_part_properties})
                # before adding missing properties to BOM part, investigate BOM part "value" property
                # check, if BOM part value contains any property symbol
                if any(symbol in bom_part_properties["value"] for symbol in property_symbols):
                    # split value
                    elements = bom_part_properties["value"].split(Definitions.BOMKW_SEPARATOR_VALUE)
                    # first element has to be the "pure value"
                    bom_part_properties.update({"value_pure":elements[0]})
                    # iterate through rest of value string elements
                    for element in elements[1:]:
                        # iterate through properties
                        for prop in database_properties:
                            # symbol not contained -> next part
                            if not prop.get_symbol() or not prop.get_symbol() in element:
                                continue
                            # update BOM part property
                            bom_part_properties.update({prop.get_name():pF.property_string_to_value(element,prop.get_type(),prop.get_symbol())})
                else:
                    bom_part_properties.update({"value_pure":bom_part_properties["value"]})
                # befor using bom_part_properties for multiple parts, remove key "ref", otherwise we override the referece of each part!
                bom_part_properties.pop("ref",None)
                for group_part in bom_part_group.get_bom_parts():
                    group_part.set_property_values(copy.deepcopy(bom_part_properties))
                # compare BOM part to each category part
                for category_part in database_category.get_elements():
                    # iterate through all properties
                    for prop in database_properties:
                        prop_name = copy.deepcopy(prop.get_name())
                        bom_prop_name = copy.deepcopy(prop.get_name())
                        if bom_prop_name == "value":
                            bom_prop_name = "value_pure"
                        # compare units
                        if prop.get_type() == Parts.PartPropertyType.UNIT:
                            if not pF.compare_value_strings_if_equal([
                                bom_part.get_property_value(bom_prop_name).replace(" ",""),
                                category_part.get_property_value(prop_name).replace(" ","")
                            ]):
                                break
                        # compare whole string
                        elif prop.get_type() == Parts.PartPropertyType.STRING or prop.get_type() == Parts.PartPropertyType.SUBSTRING:
                            # if property is empty or not defined, then it could not be compared
                            if(
                                bom_part.get_property_value(bom_prop_name) is None or
                                not bom_part.get_property_value(bom_prop_name) or
                                category_part.get_property_value(prop_name) is None or
                                not category_part.get_property_value(prop_name)
                            ):
                                continue
                            if prop.get_type() == Parts.PartPropertyType.STRING:
                                if bom_part.get_property_value(bom_prop_name).replace(" ","").lower() != category_part.get_property_value(prop_name).replace(" ","").lower():
                                    break
                            elif prop.get_type() == Parts.PartPropertyType.SUBSTRING:
                                if category_part.get_property_value(prop_name).replace(" ","").lower() not in bom_part.get_property_value(bom_prop_name).replace(" ","").lower():
                                    break
                        else:
                            # if property is not set, then it could not be compared
                            if(
                                bom_part.get_property_value(bom_prop_name) is None or
                                category_part.get_property_value(prop_name) is None
                            ):
                                continue
                            if prop.get_type() == Parts.PartPropertyType.NUMBER_MAX:
                                if category_part.get_property_value(prop_name) > bom_part.get_property_value(bom_prop_name):
                                    break
                            elif prop.get_type() == Parts.PartPropertyType.NUMBER_EQUAL:
                                if category_part.get_property_value(prop_name) != bom_part.get_property_value(bom_prop_name):
                                    break
                            elif prop.get_type() == Parts.PartPropertyType.NUMBER_MIN:
                                if category_part.get_property_value(prop_name) < bom_part.get_property_value(bom_prop_name):
                                    break
                    # match found, because loop was not aborted, so all properties match
                    else:
                        bom_part_group.add_matching_part(category_part)
                # default selection is the first part in the list, if there is at least one matching part
                for group_part in bom_part_group.get_bom_parts():
                    match = Parts.Match()
                    match.set_bom_part(group_part)
                    if bom_part_group.get_number_of_matching_parts() > 0:
                        match.set_match(bom_part_group.get_matching_part_index(0))
                    bom_part_group.add_match(match)
                # add BOM part group to category
                match_category.add_groups(bom_part_group)
            # add category
            if match_category.get_number_of_elements() > 0:
                self.match_categories.append(match_category)

    def get_match_categories(self):
        return self.match_categories

    def export(self,folder,filename):
        self.order_list_items = []
        self.order_list_groups = []
        self.order_list_distributors = []

        # create list of distributors
        for configuration in Setup.DOC:
            self.order_list_distributors.append(Parts.OrderListDristributor(configuration))

        # create one order list item for each match (matching parts must not be None and user did not removed it)
        for match_category in self.match_categories:
            for group in match_category.get_elements():
                group_attributes = copy.deepcopy(group.get_attributes())
                for match in group.get_matches():
                    attributes = group_attributes.pop(0)
                    # no matching part -> skip
                    if match.get_matching_part() is None:
                        continue
                    # user changed any atrribute checkbox -> skip
                    if any(attributes[attribute] != Setup.GUI_ITEM_ATTRIBUTES[attribute] for attribute in attributes):
                        continue
                    # ordering number not defined or empty
                    ord_number = match.get_matching_part().get_property_value("ordnum")
                    if ord_number is None:
                        continue
                    if not ord_number:
                        continue
                    self.order_list_items.append(Parts.OrderListItem(match))

        # group order list items
        for item in self.order_list_items:
            for group in self.order_list_groups:
                # if item fits to any group, then add
                if group.get_reference_item().is_equal(item):
                    group.add_item(item)
                    break
            else:
                # otherwise create new group
                new_group = Parts.OrderListGroup(item)
                self.order_list_groups.append(new_group)
                # assign order list group to distributor
                for distributor in self.order_list_distributors:
                    if distributor.get_distributor().lower() == item.get_property_values("distributor").lower():
                        distributor.add_group(new_group)
                        break
                else:
                    self.order_list_distributors[-1].add_group(new_group)

        # create export files
        for distributor in self.order_list_distributors:
            distributor.write_file(os.path.join(folder,filename + "_" + distributor.get_distributor().lower() + ".txt"))

        # create elementwise overview
        try:
            file_name = os.path.join(folder,filename + "_summarized.txt")
            fobj = open(file_name,"w")
            # write header if requested
            fobj.write(Setup.SEO_DELIMITER.join(Setup.SEO))
            fobj.write("\n")
            # write each order list item into one line
            for item in self.order_list_items:
                fobj.write(item.get_list_item_string(Setup.SEO))
                fobj.write("\n")
            # done, so close file
            fobj.close()
        except Exception as e:
            raise Exception("failed writing output to file: " + file_name + " Error: " + e.args[0]) from e

class System():
    def __init__(self):
        if not isinstance(Setup.DEFAULT_DIRECTORY,str):
            raise Exception("DEFAULT_DIRECTORY defined in settings.py is not a string")
        if not isinstance(Setup.DEFAULT_FILE,str):
            raise Exception("DEFAULT_FILE defined in settings.py is not a string")
        self.DEFAULT_DIRECTORY = Setup.DEFAULT_DIRECTORY
        self.DEFAULT_FILE = Setup.DEFAULT_FILE
        try:
            self.systems = Settings.SYSTEMS
            self.selected_system = []
            self.system_names = []
            for system in self.systems:
                self.system_names.append(system["NAME"])
                if any(param not in system for param in ["REF_SYM_IGNORE","BOMKW_REQ_PROPERTIES"]):
                    raise Exception("missing system parameter in system definition")
        except Exception as e:
            raise Exception("settings.py contains wrong system definition! Error: " + e.args[0]) from e
        self.select_system(Settings.DEFAULT_SYSTEM)

    def get_system_names(self):
        return self.system_names

    def get_name_of_selected_system(self):
        return self.selected_system["NAME"]

    def get_default_directory(self):
        return self.DEFAULT_DIRECTORY

    def get_default_file(self):
        return self.DEFAULT_FILE

    def get_ignored_ref_symbols(self):
        return self.REF_SYM_IGNORE

    def get_req_bom_part_properties(self):
        return self.BOMKW_REQ_PROPERTIES

    def select_system(self,system_name):
        self.REF_SYM_IGNORE = copy.deepcopy(Settings.REF_SYM_IGNORE)
        self.BOMKW_REQ_PROPERTIES = copy.deepcopy(Settings.BOMKW_REQ_PROPERTIES)
        for system in self.systems:
            if system_name.lower() == system["NAME"].lower():
                self.selected_system = system
                self.REF_SYM_IGNORE.extend(system["REF_SYM_IGNORE"])
                self.BOMKW_REQ_PROPERTIES.extend(system["BOMKW_REQ_PROPERTIES"])
                break
        else:
            raise Exception("System " + system_name + " not defined!")

        