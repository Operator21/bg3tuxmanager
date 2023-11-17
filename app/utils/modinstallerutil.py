import os
import shutil
from app.utils.xmlutil import XmlUtil
from app.model.mod import Mod
from app.utils.properties import BALDURSGATE_MOD_FOLDER, MOD_SETTING_LSX_PATH
from app.model.nodetype import NodeType

class ModInstallerUtil:
    @staticmethod
    def install_mods(mods: list[Mod]):
        # Modify xml of file modsetting.lsx
        xml_util = XmlUtil(MOD_SETTING_LSX_PATH)
        
        xml_util.clear_mods()
        ModInstallerUtil.clear_mod_folder()

        for mod in mods:
            # check if mod has path
            if not hasattr(mod, "path"):
                print(f"Mod has no path.")
                continue

            # Split path to check if .pak file is directly in tmp folder
            split_path = mod.path.rsplit('/', 1)
            if split_path[0].endswith("tmp"):
                pak_file_path = f"{mod.path}/{mod.Folder}.pak"
            else:
                pak_file_path = f"{split_path[0]}/{mod.Folder}.pak"

            # copy .pak file to baldurs gatemod folder
            shutil.copy(pak_file_path, BALDURSGATE_MOD_FOLDER)

            # if mod did not have info.json file, skip
            if mod.UUID == "":
                continue

            # add mod definitions to xml
            xml_util.add_nodes([mod], nodetype=NodeType.DEFINITION)

            # add mod order to xml
            xml_util.add_nodes([mod], nodetype=NodeType.ORDER)

    @staticmethod
    def clear_mod_folder():
        # clears all files from the BALDURSGATE_MOD_FOLDER.
        for filename in os.listdir(BALDURSGATE_MOD_FOLDER):
            file_path = os.path.join(BALDURSGATE_MOD_FOLDER, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
