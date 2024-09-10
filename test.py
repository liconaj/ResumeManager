from utils import *

config = Config()
gspreadsheet = GSpreadSheet(config.get("MASTER_SHEET_ID"), config.get("MASTER_SHEET_RANGE"))
db_manager = DbManager()
db_manager.set_gspreadsheet(gspreadsheet)
im = ImportManager(config, db_manager)
im.set_import_form(1)
profiles = im.get_form_profiles()
for p in profiles:
    if p["_already_imported"]:
        print(f"Ya importado {p['full_name']}")
