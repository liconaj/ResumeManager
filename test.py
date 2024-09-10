from utils import *

config = Config()
im = ImportManager(config, None)
im.set_import_form(0)
profiles = im.get_form_profiles()
print(profiles[310])