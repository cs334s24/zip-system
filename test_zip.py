# Testing file for the zip.py

import unittest
from unittest.mock import patch
import os
from io import StringIO
from zip import main, getFileIdsFromUser, searchFilesWithIds, zipSampleData, download_from_s3

class TestScript(unittest.TestCase):

    @patch('builtins.input', return_value="IHS-2005-0004, CRB-2009-0003, CRB-2006-0005")
    def test_main_positive_case(self, mock_input):
        main()
        self.assertTrue(os.path.exists("data.zip")) 
        self.assertFalse(os.path.exists("temp-data"))  

    @patch('builtins.input', return_value="")
    def test_main_empty_input(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue().strip()
            self.assertEqual(output, "Enter the file IDs separated by commas: ")

    @patch('builtins.input', return_value="IHS-2005-0004, CRB-2009-0003, CRB-2006-0005")
    def test_getFileIdsFromUser(self, mock_input):
        file_ids = getFileIdsFromUser()
        self.assertEqual(file_ids, ["IHS-2005-0004", "CRB-2009-0003", "CRB-2006-0005"])

    def test_searchFilesWithIds(self):
        file_ids = ["IHS-2005-0004", "CRB-2009-0003", "CRB-2006-0005"]
        matching_files = searchFilesWithIds(file_ids)

    def test_zipSampleData(self):
        zipSampleData()
        self.assertTrue(os.path.exists("data.zip"))

    @patch('your_script.sh.aws')
    def test_download_from_s3(self, mock_aws):
        docket_id = "IHS-2005-0004"
        download_from_s3(docket_id)
        mock_aws.assert_called_with('s3', 'cp', 's3://mirrulations-sample-data-opensearch/IHS/IHS-2005-0004', 'temp-data/data/IHS-2005-0004', '--recursive')

if __name__ == "__main__":
    unittest.main()

