import os
import shutil
import tempfile
import zipfile

def main():
    file_ids = getFileIdsFromUser()
    zipFilesWithIds(file_ids)

# Prompts the user to enter ID's for a desired file. 
#   (Ex: "IHS-2005-0004, CRB-2009-0003, CRB-2006-0005" or "CRB-2009-0003")
def getFileIdsFromUser():
    ids = input("Enter the file IDs separated by commas: ")
    return [id.strip() for id in ids.split(',')]

# Based off the ID's given search for files containing them in their file name
def searchFilesWithIds(file_ids):
    matching_files = []
    for root, dirs, files in os.walk(".", topdown=True):
        for file in files:
            for file_id in file_ids:
                if file_id in file:
                    matching_files.append(os.path.join(root, file))
    return matching_files

# Copy the files found to a temp folder
def copyFilesToTempDirectory(files):
    temp_dir = tempfile.mkdtemp()
    for file_path in files:
        relative_path = os.path.relpath(file_path, ".")
        temp_file_path = os.path.join(temp_dir, relative_path)
        os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
        shutil.copy(file_path, temp_file_path)
    return temp_dir

# Creates a zip file with files corresponding to given IDs.
# Searches for files containing specified IDs in their names and zips them.
def createZipFile(temp_dir, file_ids):
    output_zip = os.path.join(os.getcwd(), '_'.join(file_ids) + '.zip')
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, temp_dir)
                zip_file.write(file_path, relative_path)
    return output_zip

# Searches for files in the current working directory that contain the specified file IDs in their filenames.
def zipFilesWithIds(file_ids):
    matching_files = searchFilesWithIds(file_ids)
    if matching_files:
        temp_dir = copyFilesToTempDirectory(matching_files)
        try:
            output_zip = createZipFile(temp_dir, file_ids)
            print("Files with IDs '{}' zipped to {}".format(', '.join(file_ids), output_zip))
        finally:
            shutil.rmtree(temp_dir)
    else:
        print("No files found with IDs '{}'.".format(', '.join(file_ids)))

if __name__ == "__main__":
    main()
