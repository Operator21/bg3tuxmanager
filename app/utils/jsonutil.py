import json
from app.model.mod import Mod

class JsonLoader:
    @staticmethod
    def load_mods_from_file(file_path):
        with open(file_path) as json_file:
            data = json.load(json_file)
            mods = data.get('Mods', [])
            mod_objects = [Mod(**mod) for mod in mods]
            # set paths of each mode to file_path
            for mod in mod_objects:
                mod.path = file_path

            # if any mod has attribute with None value, set it to empty string
            for attr, value in mod.__dict__.items():
                if value is None:
                    setattr(mod, attr, "")
            
            return mod_objects
