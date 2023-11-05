from app.utils.archiveutil import ArchiveUtil
from app.utils.jsonutil import JsonLoader
from app.utils.modinstallerutil import ModInstallerUtil

# clear temporary files
ArchiveUtil.clear_tmp()

# paths to mod archives
path_to_mods = []


mods = []
for path_to_mod in path_to_mods:
    # get path to extracted mod files
    tmp = ArchiveUtil.extract_and_delete_archive(path_to_mod)

    # load info.json file to mod
    mods.append(JsonLoader.load_mods_from_file(f"{tmp}/info.json")[0])


# install mods
ModInstallerUtil.install_mods(mods)