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

import setup as Setup

# collect strings for each language
languages = {}

# english
languages.update({"en":{
    "window_title":"Order List Generator",
    "button_bom":"BOM-file",
    "button_bom_tooltip":"Choose BOM-file",
    "button_database":"lists of\nordering numbers",
    "button_database_tooltip":"Select the folder containg the lists with the orderig numbers",
    "button_regroup":"group equal\npairs",
    "button_regroup_tooltip":"Group identical pairs of BOM-parts and assigned ordering number",
    "checkbox_grouped":"group parts",
    "button_export":"generate\norder lists",
    "button_export_tooltip":"Create distributor specific order lists based on the selected pairs",
    "button_generate":"Search pairs",
    "button_generate_tooltip":"Search for known ordering numbers",
    "label_hint":'Choose a BOM-file and the path containing the lists with the ordering numbers and press "Search pairs"',
    "button_close":"Close",
    "button_close_tooltip":"Close application",
    "status_bar_msg_done":"Done...",
    "status_bar_msg_error":"Error!",
    "status_bar_msg_search_running":"Search running...",
    "status_bar_msg_search_finished":"Search finished...",
    "status_bar_msg_bom_file":"choose BOM-file...",
    "status_bar_msg_bom_sel_file":"Choosen BOM-file: ",
    "status_bar_msg_database_folder":"Choose folder...",
    "status_bar_msg_database_sel_folder":"Choosen folder: ",
    "file_dialog_bom_name":"BOM-file",
    "file_dialog_bom_type":"csv-files (*.csv);;All Files (*)",
    "file_dialog_database_name":"Ordering numbers",
    "error":"Error!",
    "error_msg_file_and_folder":"Please choose a BOM-file and the folder containing the lists with the ordering numbers!",
    "PTI_category_others_description":"others"
}})

# german
languages.update({"de":{
    "window_title":"Bestelllistengenerator",
    "button_bom":"St??ckliste",
    "button_bom_tooltip":"St??ckliste w??hlen",
    "button_database":"Bestellnummern",
    "button_database_tooltip":"Ordner mit den Bestellnummern w??hlen",
    "button_regroup":"gleiche Zuordnungen\nzusammenfassen",
    "button_regroup_tooltip":"Zusammenfassen von identischen St??cklistenteil-Bestellnummer-Zuordnungen",
    "checkbox_grouped":"Bauteile gruppieren",
    "button_export":"generiere\nBestelllisten",
    "button_export_tooltip":"Erstellung lieferantenspezifischer Bestelllisten anhand der gew??hlten Paare",
    "button_generate":"Suche Paare",
    "button_generate_tooltip":"Suche nach bekannten Bestellnummern",
    "label_hint":'W??hle eine St??ckliste und den Pfad zu den Bestelllisten und dr??cke auf "Suche Paare"',
    "button_close":"Schlie??en",
    "button_close_tooltip":"Anwendung schlie??en",
    "status_bar_msg_done":"Erledigt...",
    "status_bar_msg_error":"Fehler!",
    "status_bar_msg_search_running":"Suche l??uft...",
    "status_bar_msg_search_finished":"Suche beendet...",
    "status_bar_msg_bom_file":"w??hle St??ckliste...",
    "status_bar_msg_bom_sel_file":"gew??hlte St??ckliste: ",
    "status_bar_msg_database_folder":"w??hle Ordnerpfad...",
    "status_bar_msg_database_sel_folder":"gew??hlter Ordner: ",
    "file_dialog_bom_name":"St??ckliste",
    "file_dialog_bom_type":"csv-Dateien (*.csv);;All Files (*)",
    "file_dialog_database_name":"Bestellnummern",
    "error":"Fehler!",
    "error_msg_file_and_folder":"Bitte St??ckliste und Ordner mit den Bestellnummern w??hlen!",
    "PTI_category_others_description":"weitere Bauteile"
}})

# return requested string
def get_string(key):
    return languages[Setup.LANGUAGE][key]
