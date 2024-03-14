import unittest
from unittest.mock import patch
from io import StringIO
from zip import getFileIdsFromUser, searchFilesWithIds, zipSampleData

class TestScript(unittest.TestCase):
    @patch('builtins.input', side_effect=['IHS-2005-0004, CRB-2009-0003, CRB-2006-0005'])
    def test_getFileIdsFromUser(self, mock_input):
        expected_ids = ['IHS-2005-0004', 'CRB-2009-0003', 'CRB-2006-0005']
        result = getFileIdsFromUser()
        self.assertEqual(result, expected_ids)

    def test_searchFilesWithIds(self):
        file_ids = ['IHS-2005-0004', 'CRB-2009-0003']
        expected_files = ['temp-data/data/IHS-2005-0004/somefile.txt']
        result = searchFilesWithIds(file_ids)
        self.assertEqual(result, expected_files)

    def test_zipSampleData(self):
        with patch('zipfile.ZipFile') as mock_zipfile:
            zipSampleData()
            mock_zipfile.assert_called_once_with('data.zip', 'w')

if __name__ == '__main__':
    unittest.main()
