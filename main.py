from app.model.mod import Mod
from app.utils.archiveutil import ArchiveUtil
from app.utils.jsonutil import JsonLoader
from app.utils.modinstallerutil import ModInstallerUtil
from app.utils.scriptextenderutil import ScriptExtenderUtil

# clear temporary files
ArchiveUtil.clear_tmp()

# check if script extender exists
if ScriptExtenderUtil.is_extender_installed():
    print("Script extender was detected")
else:
    print("Script extender was not detected")
    answer = input("Do you want to install it? (y/n): ")
    if answer.lower() == "y":
        ScriptExtenderUtil.try_to_download_from_github()

        if ScriptExtenderUtil.is_os_linux():
            print("It looks you are using Linux, very good. Make sure you have following line in your steam launch parameters, otherwise extender will not work:\n\n\tWINEDLLOVERRIDES=\"DWrite.dll=n,b\" PROTON_NO_ESYNC=1 %command%\n")


# paths to mod archives
path_to_mods = []


mods = []
for path_to_mod in path_to_mods:
    # get path to extracted mod files
    tmp = ArchiveUtil.extract_and_delete_archive(path_to_mod)

    result = JsonLoader.load_mods_from_file(f"{tmp[ArchiveUtil.PATH_TO_EXTRACTED_FOLDER]}/info.json")

    if result is None:
        # mod does not have info.json file
        mod = Mod(Folder=tmp[ArchiveUtil.FOLDER_NAME])
        mod.path = tmp[ArchiveUtil.PATH_TO_EXTRACTED_FOLDER]
        mods.append(mod)
        continue

    # check if tmp folder corresponds with loaded info
    if tmp[ArchiveUtil.FOLDER_NAME] != result[0].Folder:
        # info file is set incorrectly, correct it
        result[0].Folder = tmp[ArchiveUtil.FOLDER_NAME]

    # load info.json file to mod
    mods.append(result[0])


# install mods
ModInstallerUtil.install_mods(mods)