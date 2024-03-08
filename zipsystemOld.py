import zipfile
import os

#Below is what the solution was of someone attempting to zip a file, but I prefer option 2

myfilepath = '/tmp/%s' % self.file_name
myzippath = myfilepath.replace('.xml', '.zip')

zipfile.ZipFile(myzippath, 'w').write(open(myfilepath).read())

#Below is what I found across some researching and is what makes more sense to me right now.

def zip_file(file_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(file_path, os.path.basename(file_path))

file_to_zip = "The file path would be stored here for the file you would wanna zip"
zip_file_path = "This is the file path you would want the zip to be sent to "
zip_file(file_to_zip, zip_file_path) # This just calls like any other function
