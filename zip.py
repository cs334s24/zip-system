import os
import shutil
import tempfile
import zipfile

def main() :
    inputFolder = "sample-data"
    zipFolder(inputFolder)

def zipFolder(inputFolder):
    # Create a temporary directory to store files and directories
    tempDir = tempfile.mkdtemp()
    try:
        # Copy the entire folder structure to the temporary directory
        shutil.copytree(inputFolder, os.path.join(tempDir, os.path.basename(inputFolder)))
        # Determine the output zip file name
        outputZip = os.path.join(os.getcwd(), os.path.basename(inputFolder) + '.zip')
        # Create a zip file
        with zipfile.ZipFile(outputZip, 'w', zipfile.ZIP_DEFLATED) as zipFile:
            # Iterate over the directory structure and add each file and directory to the zip file
            for root, dirs, files in os.walk(tempDir):
                for file in files:
                    filePath = os.path.join(root, file)
                    relativePath = os.path.relpath(filePath, tempDir)
                    zipFile.write(filePath, relativePath)
        print("Files zipped to " + outputZip)
    finally:
        # Clean up the temporary directory
        shutil.rmtree(tempDir)

if __name__ == "__main__" :
    main()