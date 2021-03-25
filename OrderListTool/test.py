import dispatcher as Dispatcher
import settings as Settings

dispatcher = Dispatcher.Dispatcher()
dispatcher.set_bom_file_path(Settings.DEFAULT_FILE)
dispatcher.set_database_path(Settings.DEFAULT_DIRECTORY)

# dispatcher.create_part_templates()
# dispatcher.assign_database_files_to_templates()
# dispatcher.get_part_template_properties()
# dispatcher.read_database()
# dispatcher.read_bom_file()
# dispatcher.group_bom_parts()
dispatcher.find_matches()
print("done")
