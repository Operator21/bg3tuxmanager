import os
import shutil
import requests
import zipfile
from app.utils.properties import GAME_BIN_PATH


class ScriptExtenderUtil:
    game_bin_path = GAME_BIN_PATH
    repo_url = "Norbyte/bg3se"
    tmp_folder = "app/utils/tmp"
    
    @staticmethod
    def is_extender_installed():
        """
        This static method checks if DWrite.dll file exists in the game_bin_path.
        """
        dwrite_dll_path = os.path.join(ScriptExtenderUtil.game_bin_path, "DWrite.dll")
        return os.path.exists(dwrite_dll_path)
    
    @staticmethod
    def try_to_download_from_github():
        """
        This static method downloads the latest version of script extender from GitHub.
        """

        api_response = requests.get(f"https://api.github.com/repos/{ScriptExtenderUtil.repo_url}/releases/latest")

        if api_response.status_code == 200:
            # get download url
            latest_release = api_response.json()
            download_url = latest_release['assets'][0]['browser_download_url']

            # download script extender
            download_response = requests.get(download_url)
            if download_response.status_code == 200:
                # download zip from download url and extract it to temporary folder
                
                # create temporary folder if it doesn't exist
                if not os.path.exists(ScriptExtenderUtil.tmp_folder):
                    os.makedirs(ScriptExtenderUtil.tmp_folder)

                # write zip to temporary folder
                with open(f"{ScriptExtenderUtil.tmp_folder}/scriptextender.zip", "wb") as file:
                    file.write(download_response.content)
                
                # extract zip
                with zipfile.ZipFile(f"{ScriptExtenderUtil.tmp_folder}/scriptextender.zip", 'r') as zip_ref:
                    zip_ref.extractall(ScriptExtenderUtil.tmp_folder)

                # delete zip
                os.remove(f"{ScriptExtenderUtil.tmp_folder}/scriptextender.zip")

                # copy extracted DWrite.dll file to game_bin_path
                shutil.copy(f"{ScriptExtenderUtil.tmp_folder}/DWrite.dll", ScriptExtenderUtil.game_bin_path)

                # delete temporary folder
                shutil.rmtree(ScriptExtenderUtil.tmp_folder)

    @staticmethod
    def is_os_linux():
        """
        This static method checks if the operating system is Linux.
        """
        return os.name == 'posix'