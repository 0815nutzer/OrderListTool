import copy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QFrame,
    QHeaderView,
    QSizePolicy
)

import definitions as Definitions
import setup as Setup
import settings as Settings
import parts as Parts

class Visualization():
    def __init__(self,dispatcher,window_settings):
        self.dispatcher = dispatcher
        self.window_settings = window_settings
        self.layout = QVBoxLayout()
        self.category_views = []

    def get_visualization(self):
        self.category_views = []
        # QWidget().setLayout(self.layout)
        self.layout = QVBoxLayout()
        for category in self.dispatcher.get_match_categories():
            self.category_views.append(CategoryView(category,self.window_settings["view_grouped"]))
        for view in self.category_views:
            self.layout.addLayout(view.get_view())
        return self.layout

class CategoryView():
    def __init__(self,category,grouped=True):
        if not isinstance(category,Parts.Category):
            raise Exception("category is not an instance of class Category")
        if not isinstance(grouped,bool):
            raise Exception("grouped has to be a boolean")
        self.category = category
        self.grouped = grouped
        self.main_layout = QVBoxLayout()
        self.group_views = []
        # self.build_view()

    def build_view(self):
        self.group_views = []
        show_header = True
        for group in self.category.get_elements():
            self.group_views.append(GroupView(group,self.category,self.grouped,show_header))
            show_header = False

    def get_view(self):
        self.main_layout = QVBoxLayout()
        # category label
        self.label_category = QLabel(self.category.get_part_template().get_description().upper())
        self.label_category.setStyleSheet("font-weight: bold")
        self.main_layout.addWidget(self.label_category)
        # groups
        self.build_view()
        for view in self.group_views:
            self.main_layout.addLayout(view.get_layout())
        return self.main_layout

class GroupView():
    TABLE_WIDGET_ITEM_TYPE_BOM = 2000
    TABLE_WIDGET_ITEM_TYPE_QNTY = 2100
    TABLE_WIDGET_ITEM_TYPE_CHECKBOX = 3000
    TABLE_WIDGET_ITEM_TYPE_PART_SELECTED = 4000
    TABLE_WIDGET_ITEM_TYPE_PART_MATCH = 5000

    def __init__(self,group,category,grouped=True,show_header=False):
        if not isinstance(group,Parts.PartGroup):
            raise Exception("group is not an instance of class PartGroup")
        if not isinstance(category,Parts.Category):
            raise Exception("category is not an instance of class Category")
        if not isinstance(grouped,bool):
            raise Exception("grouped has to be a boolean")
        self.group = group
        self.category = category
        self.grouped = grouped
        self.tables = []
        self.main_layout = QVBoxLayout()
        self.show_header = show_header
        # if self.grouped:
        #     self.build_view(self.group.get_match(0),self.group.get_group_attributes(),show_header)
        # else:
        #     for i in range(self.group.get_number_of_bom_parts()):
        #         self.build_view(self.group.get_match(i),self.group.get_attributes(i),show_header)
        #         show_header = False

    def get_layout(self):
        QWidget().setLayout(self.main_layout)
        self.main_layout = QVBoxLayout()
        # build tables
        self.tables = []
        if self.grouped:
            self.build_view(self.group.get_match(0),self.group.get_group_attributes(),self.show_header)
        else:
            for i in range(self.group.get_number_of_bom_parts()):
                self.build_view(self.group.get_match(i),self.group.get_attributes(i),self.show_header)
                self.show_header = False
        # fill layout
        for table in self.tables:
            self.main_layout.addWidget(table)
        return self.main_layout

    def build_view(self,match,attributes,show_header):
        table = ItemQTableWidget()
        if self.grouped:
            table.set_group(self.group)
        else:
            table.set_match(match)
            table.set_attributes(attributes)
        # set up table
        cnt_columns = len(Definitions.BOMKW_PART_PROPERTIES)+len(attributes)+len(self.category.get_part_template().get_all_properties())
        if self.grouped:
            # quantity column
            cnt_columns += 1
        if self.group.get_number_of_matching_parts() <= 1:
            cnt_rows = 1
        else:
            cnt_rows = self.group.get_number_of_matching_parts() + 1
        table.setRowCount(cnt_rows)
        table.setColumnCount(cnt_columns)
        row = 0
        column_offset = 0
        # add BOM part data
        bom_part_properties = copy.deepcopy(match.get_bom_part().get_all_properties())
        # if showed grouped, then add all references
        if self.grouped:
            refs = ", ".join([part.get_property_value("ref") for part in self.group.get_bom_parts()])
            bom_part_properties["ref"]=refs
        for rp in Definitions.BOMKW_PART_PROPERTIES:    # rp ... requested properties
            item = QTableWidgetItem(type=self.TABLE_WIDGET_ITEM_TYPE_BOM)
            item.setText(str(bom_part_properties[rp]))
            table.setItem(row,column_offset,item)
            if rp == "ref":
                table.setColumnWidth(column_offset,Definitions.GUI_WIDTH_ITEM_REF)
            elif rp == "value":
                table.setColumnWidth(column_offset,Definitions.GUI_WIDTH_ITEM_VALUE)
            elif rp == "package":
                table.setColumnWidth(column_offset,Definitions.GUI_WIDTH_ITEM_PACKAGE)
            else:
                table.setColumnWidth(column_offset,Definitions.GUI_WIDTH_ITEM_OTHERS)
            column_offset += 1
        # add quantity (only grouped view)
        if self.grouped:
            item = QTableWidgetItem(type=self.TABLE_WIDGET_ITEM_TYPE_QNTY)
            item.setText(str(self.group.get_number_of_bom_parts()))
            table.setItem(row,column_offset,item)
            table.setColumnWidth(column_offset,Definitions.GUI_WIDTH_ITEM_QNTY)
            column_offset += 1
        # attribute checkboxes
        if self.grouped:
            deviating_group_attributes = self.group.get_deviating_group_attributes()
        for attribute in attributes:
            checkbox = QTableWidgetItem(type=self.TABLE_WIDGET_ITEM_TYPE_CHECKBOX)
            checkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            if attributes[attribute]:
                checkbox.setCheckState(Qt.Checked)
            else:
                checkbox.setCheckState(Qt.Unchecked)
            checkbox.setData(Qt.UserRole,attribute)
            table.setItem(row, column_offset,checkbox)
            # color background if grouped view and group elements differ from group attributes
            if self.grouped:
                if deviating_group_attributes[attribute]:
                    table.item(row, column_offset).setBackground(QColor(255,204,204))
            # table.setColumnWidth(column_offset, Definitions.GUI_WIDTH_ITEM_CHECKBOX)
            column_offset += 1 # at the end it points to the first selected part column
        table.set_column_offset(column_offset)
        # fill line with matching part
        if match.get_matching_part() is not None:
            col = 0
            for value in match.get_matching_part().get_all_property_values():
                item = QTableWidgetItem(self.TABLE_WIDGET_ITEM_TYPE_PART_SELECTED)
                item.setText(str(value))
                table.setItem(row,col+column_offset,item)
                table.setColumnWidth(col+column_offset,Definitions.GUI_WIDTH_ITEM_OTHERS)
                if self.group.get_number_of_matching_parts() == 1:
                    table.item(row,col+column_offset).setBackground(QColor(204,255,204))
                elif self.group.get_number_of_matching_parts() > 1:
                    table.item(row,col+column_offset).setBackground(QColor(255,255,204))
                col += 1
        # no matching part -> add empty items, that view looks nice
        else:
            col = 0
            for value in self.category.get_part_template().get_names_of_all_properties():
                item = QTableWidgetItem(self.TABLE_WIDGET_ITEM_TYPE_PART_SELECTED)
                item.setText("")
                table.setItem(row,col+column_offset,item)
                table.setColumnWidth(col+column_offset,Definitions.GUI_WIDTH_ITEM_OTHERS)
                col += 1
        # if there are more than one matching part, add one line for each matching part
        if self.group.get_number_of_matching_parts() > 1:
            row += 1
            for part in self.group.get_matching_parts():
                col = 0
                for value in part.get_all_property_values():
                    item = QTableWidgetItem(self.TABLE_WIDGET_ITEM_TYPE_PART_MATCH)
                    item.setText(str(value))
                    table.setItem(row,col+column_offset,item)
                    col += 1
                table.setRowHidden(row,True)
                row += 1
        # add header labels
        if show_header:
            labels = copy.deepcopy(Definitions.BOMKW_PART_PROPERTIES)
            if self.grouped:
                labels.append("Menge")
            labels.extend([keys for keys in attributes])
            labels.extend(self.category.get_part_template().get_names_of_all_properties())
            table.setHorizontalHeaderLabels([label.upper() for label in labels])
            table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        else:
            table.horizontalHeader().hide()
        # resize rows
        table.verticalHeader().setMinimumSectionSize(Definitions.GUI_HEIGHT_ITEM)
        table.resizeRowsToContents()
        # determine width and height
        table_width = 0
        table_height = 0
        for i in range(table.columnCount()):
            table_width += table.columnWidth(i)
        for i in range(table.rowCount()):
            table_height += table.rowHeight(i)
        if not table.horizontalHeader().isHidden():
            table_height += table.horizontalHeader().height()
        table.verticalHeader().hide()
        table.setFrameStyle(QFrame.NoFrame)
        table.setShowGrid(False)
        table.setAlternatingRowColors(True)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.setFixedSize(table_width,table_height)
        table.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.clearFocus()
        table.clearSelection()
        table.itemClicked.connect(self.clicked)
        self.tables.append(table)

    def clicked(self,item):
        table = item.tableWidget()
        if item.type() == self.TABLE_WIDGET_ITEM_TYPE_CHECKBOX:
            if item.checkState() == Qt.Unchecked:
                checked = False
            else:
                checked = True
            attribute_name = item.data(Qt.UserRole)
            if self.grouped:
                for i in range(self.group.get_number_of_attributes()):
                    self.group.set_attributes({attribute_name:checked},i)
                # remove color hint
                item.setBackground(QColor(255,255,255))
            else:
                att = table.get_attributes()
                att[attribute_name] = checked
        elif item.type() == self.TABLE_WIDGET_ITEM_TYPE_PART_SELECTED or item.type() == self.TABLE_WIDGET_ITEM_TYPE_PART_MATCH:
            row_index = item.row()
            if row_index == 0:
                for i in range(1,table.rowCount()):
                    if table.isRowHidden(i):
                        table.setRowHidden(i,False)
                    else:
                        table.setRowHidden(i,True)
            else:
                # change selected parts
                if self.grouped:
                    for match in self.group.get_matches():
                        match.set_match(self.group.get_matching_part_index(row_index - 1))
                else:
                    table.get_match().set_match(self.group.get_matching_part_index(row_index - 1))
                # update first table row
                col = 0
                for value in self.group.get_matching_part_index(row_index - 1).get_all_property_values():
                    table.item(0,col + table.get_column_offset()).setText(str(value))
                    col += 1
                for i in range(1,table.rowCount()):
                    table.setRowHidden(i,True)
        # resize rows
        table.clearFocus()
        table.clearSelection()
        table.verticalHeader().setMinimumSectionSize(Definitions.GUI_HEIGHT_ITEM)
        table.resizeRowsToContents()
        # compute final size
        table_width = 0
        table_height = 0
        for i in range(table.columnCount()):
            table_width += table.columnWidth(i)
        for i in range(table.rowCount()):
            table_height += table.rowHeight(i)
        if not table.horizontalHeader().isHidden():
            table_height += table.horizontalHeader().height()
        table.setFixedSize(table_width,table_height)
        table.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        return

class ItemQTableWidget(QTableWidget):
    def __init__(self):
        super().__init__()
        self.group = None
        self.match = None
        self.attributes = None  # only required when part view is not grouped
        self.column_offset = 0

    def set_group(self,group):
        if not isinstance(group,Parts.PartGroup):
            raise Exception("group is not an instance of class PartGroup")
        self.group = group

    def set_match(self,match):
        if not isinstance(match,Parts.Match):
            raise Exception("match is not an instance of class Match")
        self.match = match

    def set_attributes(self,attributes):
        self.attributes = attributes

    def get_group(self):
        return self.group

    def get_match(self):
        return self.match

    def get_attributes(self):
        return self.attributes

    def set_column_offset(self,offset):
        if not isinstance(offset,int):
            raise Exception("ofset has to be an integer")
        self.column_offset = offset

    def get_column_offset(self):
        return self.column_offset