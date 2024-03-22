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
    total_size_limit=500000000 # Set a total size limit (default: 500MB)
    if not os.path.exists("temp-data/data"):
        os.makedirs("temp-data/data")

    docket_dir = "temp-data/data/" + docket_id
    print(f"Docker dir for {docket_id} is {docket_dir}.")
    if os.path.exists(docket_dir):
        print(f"Data for {docket_id} already exists, skipping download.")
        return False  # Skip if the directory already exists

    os.makedirs(docket_dir)

    # Download files recursively from S3
    docket_info = docket_id.split("-")
    sh.aws('s3', 'cp', 's3://mirrulations-sample-data-opensearch/' + docket_info[0] + '/' + docket_id, docket_dir, '--recursive')
    print(f"Docker_info = {docket_info}")

    # Calculate total size of downloaded files
    total_size = sum(os.path.getsize(os.path.join(root, file)) for root, _, files in os.walk(docket_dir) for file in files)

    if total_size > total_size_limit:
        print(f"Downloaded size ({total_size} bytes) exceeded limit ({total_size_limit} bytes). Deleting downloaded data.")
        sh.rm('-r', docket_dir)  # Delete downloaded data if limit exceeded
        return True
    else:
        return False


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


# Zip temp-data into data.zip keeping temp-data/ as the root directory
def zipSampleData(name_id, docket_ids):
    count = 0
    zip_file_name = f"{name_id}.zip"  # Define the name of the zip file
    with zipfile.ZipFile(zip_file_name, 'w') as zipf:
        for docket_id in docket_ids:
            print(f"Docket Ids: {docket_ids}")
            print(f"Current Docket Id: {docket_id}")
            docket_dir = f"temp-data/data/{docket_id}"
            for root, _, files in os.walk(docket_dir):  
                count += 1
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, "temp-data")) 
                    print(f"Added file to zip: {file_path}")
                    print(f"Dir Count: {count}")
    print(f"{zip_file_name} has been created")


if __name__ == "__main__":
    main()
