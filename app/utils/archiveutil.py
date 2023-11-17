import os
import shutil
import zipfile
import random
import string

class ArchiveUtil:
    PATH_TO_EXTRACTED_FOLDER = "path_to_extracted_mod"
    FOLDER_NAME = "folder_name"

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
            temp_extract_dir = os.path.join(sub_dir, 'temp_extract')
            os.makedirs(temp_extract_dir, exist_ok=True)
            zip_ref.extractall(temp_extract_dir)

        extracted_contents = os.listdir(temp_extract_dir)

        # If the archive only contains one folder, move its contents up
        if len(extracted_contents) == 1 and os.path.isdir(os.path.join(temp_extract_dir, extracted_contents[0])):
            inner_dir = os.path.join(temp_extract_dir, extracted_contents[0])
            for item in os.listdir(inner_dir):
                shutil.move(os.path.join(inner_dir, item), sub_dir)
        else:
            # If there are more items or the sole item is a file, move them to the sub_dir
            for item in extracted_contents:
                shutil.move(os.path.join(temp_extract_dir, item), sub_dir)

        # Remove the temporary extraction directory
        shutil.rmtree(temp_extract_dir)

        # Delete the archive
        os.remove(os.path.join(sub_dir, os.path.basename(path_to_zip)))

        # Modify path so extracted folder contains .pak file
        result = ArchiveUtil.find_pak_file(sub_dir)

        return result

    @staticmethod
    def clear_tmp():
        path = os.path.join(os.path.dirname(__file__), 'tmp')

        if not os.path.exists(path):
            return
        
        shutil.rmtree(os.path.join(os.path.dirname(__file__), 'tmp'))    

    @staticmethod
    def find_pak_file(path):
        # Check if the given directory contains a .pak file
        for file in os.listdir(path):
            if file.endswith('.pak'):
                return {
                    ArchiveUtil.PATH_TO_EXTRACTED_FOLDER: path,
                    ArchiveUtil.FOLDER_NAME: os.path.splitext(file)[0]
                }

        # If no .pak file is found in the given directory, search the subdirectories
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.pak'):
                    return {
                        ArchiveUtil.PATH_TO_EXTRACTED_FOLDER: root,
                        ArchiveUtil.FOLDER_NAME: os.path.splitext(file)[0]
                    }

        # Return None if no .pak file is found
        return None
            
        
        
