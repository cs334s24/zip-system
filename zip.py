import os
import zipfile
import sh


def main():
    file_ids = getFileIdsFromUser()
    if os.path.exists("temp-data"):
        sh.rm('-r', 'temp-data')
    for file_id in file_ids:
        print(file_id)
        download_from_s3(file_id)
    zipSampleData()
    print("data.zip has been created")
    sh.rm('-r', 'temp-data')
    putZipToS3('data.zip')
    sh.rm('data.zip')


# put zip file to s3 bucket zip-system-put
def putZipToS3(zip):
    sh.aws('s3', 'cp', zip, 's3://zip-system-put')


# Download the sample data from S3
def download_from_s3(docket_id):
    if not os.path.exists("temp-data/data"):
        os.mkdir("temp-data")
        os.mkdir("temp-data/data")
    os.mkdir("temp-data/data/" + docket_id)
    docket_info = docket_id.split("-")
    sh.aws('s3', 'cp', 's3://mirrulations-sample-data-opensearch/' + docket_info[0] + '/' + docket_id, 'temp-data/data/' + docket_id, '--recursive')


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


# Zip temp-data into data.zip keeping data/ as the root directory
def zipSampleData():
    with zipfile.ZipFile('data.zip', 'w') as zipf:
        for root, dirs, files in os.walk("temp-data"):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), "temp-data"))


if __name__ == "__main__":
    main()
