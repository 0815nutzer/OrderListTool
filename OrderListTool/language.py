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
    "button_bom":"Stückliste",
    "button_bom_tooltip":"Stückliste wählen",
    "button_database":"Bestellnummern",
    "button_database_tooltip":"Ordner mit den Bestellnummern wählen",
    "button_regroup":"gleiche Zuordnungen\nzusammenfassen",
    "button_regroup_tooltip":"Zusammenfassen von identischen Stücklistenteil-Bestellnummer-Zuordnungen",
    "checkbox_grouped":"Bauteile gruppieren",
    "button_export":"generiere\nBestelllisten",
    "button_export_tooltip":"Erstellung lieferantenspezifischer Bestelllisten anhand der gewählten Paare",
    "button_generate":"Suche Paare",
    "button_generate_tooltip":"Suche nach bekannten Bestellnummern",
    "label_hint":'Wähle eine Stückliste und den Pfad zu den Bestelllisten und drücke auf "Suche Paare"',
    "button_close":"Schließen",
    "button_close_tooltip":"Anwendung schließen",
    "status_bar_msg_done":"Erledigt...",
    "status_bar_msg_error":"Fehler!",
    "status_bar_msg_search_running":"Suche läuft...",
    "status_bar_msg_search_finished":"Suche beendet...",
    "status_bar_msg_bom_file":"wähle Stückliste...",
    "status_bar_msg_bom_sel_file":"gewählte Stückliste: ",
    "status_bar_msg_database_folder":"wähle Ordnerpfad...",
    "status_bar_msg_database_sel_folder":"gewählter Ordner: ",
    "file_dialog_bom_name":"Stückliste",
    "file_dialog_bom_type":"csv-Dateien (*.csv);;All Files (*)",
    "file_dialog_database_name":"Bestellnummern",
    "error":"Fehler!",
    "error_msg_file_and_folder":"Bitte Stückliste und Ordner mit den Bestellnummern wählen!",
    "PTI_category_others_description":"weitere Bauteile"
}})

# return requested string
def get_string(key):
    return languages[Setup.LANGUAGE][key]
