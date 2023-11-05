import os
import shutil
import zipfile
import random
import string

class ArchiveUtil:
    @staticmethod
    def extract_and_delete_archive(path_to_zip):
        # Create a temporary directory next to the script
        temp_dir = os.path.join(os.path.dirname(__file__), 'tmp')
        os.makedirs(temp_dir, exist_ok=True)

        # Generate a random string of 11 characters
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=11))

        # Create a subdirectory with the name of the archive combined with the random string
        archive_name = os.path.splitext(os.path.basename(path_to_zip))[0]
        sub_dir = os.path.join(temp_dir, f"{archive_name}_{random_str}")

        os.makedirs(sub_dir, exist_ok=True)

        # Copy the archive to the subdirectory
        shutil.copy(path_to_zip, sub_dir)

        # Extract the archive
        with zipfile.ZipFile(os.path.join(sub_dir, os.path.basename(path_to_zip)), 'r') as zip_ref:
            zip_ref.extractall(sub_dir)

        # Delete the archive
        os.remove(os.path.join(sub_dir, os.path.basename(path_to_zip)))

        # return the subdirectory
        return sub_dir

    @staticmethod
    def clear_tmp():
        shutil.rmtree(os.path.join(os.path.dirname(__file__), 'tmp'))
