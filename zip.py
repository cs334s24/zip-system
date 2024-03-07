import os
import shutil
import tempfile
import zipfile

def main():
    file_id = getFileIdFromUser()
    zipFilesWithId(file_id)

def getFileIdFromUser():
    return input("Enter the file ID to search for: ")

def searchFilesWithId(file_id):
    matching_files = []
    for root, dirs, files in os.walk(".", topdown=True):
        for file in files:
            if file_id in file:
                matching_files.append(os.path.join(root, file))
    return matching_files

def copyFilesToTempDirectory(files):
    temp_dir = tempfile.mkdtemp()
    for file_path in files:
        relative_path = os.path.relpath(file_path, ".")
        temp_file_path = os.path.join(temp_dir, relative_path)
        os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
        shutil.copy(file_path, temp_file_path)
    return temp_dir

def createZipFile(temp_dir, file_id):
    output_zip = os.path.join(os.getcwd(), file_id + '.zip')
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, temp_dir)
                zip_file.write(file_path, relative_path)
    return output_zip

def zipFilesWithId(file_id):
    matching_files = searchFilesWithId(file_id)
    if matching_files:
        temp_dir = copyFilesToTempDirectory(matching_files)
        try:
            output_zip = createZipFile(temp_dir, file_id)
            print("Files with ID '{}' zipped to {}".format(file_id, output_zip))
        finally:
            shutil.rmtree(temp_dir)
    else:
        print("No files found with ID '{}'.".format(file_id))

if __name__ == "__main__":
    main()