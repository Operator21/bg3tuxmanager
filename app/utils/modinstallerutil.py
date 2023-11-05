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

        for mod in mods:
            # get path to .pak file from mod.path (which contains path to info.json)
            pak_file_path = mod.path.rsplit('/', 1)[0] + f"/{mod.Folder}.pak"

            # copy .pak file to baldurs gatemod folder
            shutil.copy(pak_file_path, BALDURSGATE_MOD_FOLDER)

            # add mod definitions to xml
            xml_util.add_nodes([mod], nodetype=NodeType.DEFINITION)

            # add mod order to xml
            xml_util.add_nodes([mod], nodetype=NodeType.ORDER)
