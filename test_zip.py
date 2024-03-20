import os
import zipfile
import sh
from zip import zipSampleData, putZipToS3, download_from_s3, getFileIdsFromUser, searchFilesWithIds

def test_zipSampleData():
   zipSampleData()
   assert os.path.exists("data.zip")
   os.remove("data.zip")

def test_getFileIdsFromUser():
   test_input = "IHS-2005-0004, CRB-2009-0003, CRB-2006-0005"
   expected_output = ["IHS-2005-0004", "CRB-2009-0003", "CRB-2006-0005"]
   assert getFileIdsFromUser(test_input) == expected_output

def test_searchFilesWithIds():
   test_file_ids = ["IHS-2005-0004", "CRB-2009-0003"]
   expected_matching_files = ["./path/to/IHS-2005-0004-file.txt", "./path/to/CRB-2009-0003-file.txt"]
   assert searchFilesWithIds(test_file_ids) == expected_matching_files

def test_putZipToS3():
   putZipToS3("data.zip")
   assert sh.aws('s3', 'cp', 'data.zip', 's3://zip-system-put') == 0

def test_download_from_s3():
   test_docket_id = "IHS-2005-0004"
   download_from_s3(test_docket_id)
   assert os.path.exists("temp-data/data/IHS-2005-0004")
   sh.rm('-r', 'temp-data')