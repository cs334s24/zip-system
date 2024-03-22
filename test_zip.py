import os
from unittest.mock import patch
from unittest import TestCase
from io import StringIO
import unittest
import sh
import subprocess
from zip import (
    getFileIdsFromUser,
    searchFilesWithIds,
    zipSampleData,
    download_from_s3,
    putZipToS3,
)

class TestZipFunctions(unittest.TestCase):

    def test_getFileIdsFromUser(self):
        with patch('builtins.input', return_value='IHS-2005-0004, CRB-2009-0003'):
            result = getFileIdsFromUser()
            self.assertEqual(result, ['IHS-2005-0004', 'CRB-2009-0003'])

    def test_getFileIdsFromUser_empty(self):
        with patch('builtins.input', return_value=''):
            result = getFileIdsFromUser()
            self.assertEqual(result, [''])
    
    def test_getFileIdsFromUser_single(self):
        with patch('builtins.input', return_value='IHS-2005-0004'):
            result = getFileIdsFromUser()
            self.assertEqual(result, ['IHS-2005-0004'])
    
    def test_getFileIdsFromUser_spaces(self):
        with patch('builtins.input', return_value='IHS-2005-0004, CRB-2009-0003, CRB-2006-0005'):
            result = getFileIdsFromUser()
            self.assertEqual(result, ['IHS-2005-0004', 'CRB-2009-0003', 'CRB-2006-0005'])

    @patch('sh.aws')
    def test_putZipToS3(self, mocked_aws):
        putZipToS3('test.zip')
        mocked_aws.assert_called_once_with('s3', 'cp', 'test.zip', 's3://zip-system-put')

    @patch('sh.aws')
    def test_download_from_s3_exists(self, mocked_aws):
        with patch('os.path.exists', return_value=True):
            result = download_from_s3('IHS-2005-0004')
            self.assertEqual(result, False)
            mocked_aws.assert_not_called()

    def test_searchFilesWithIds_empty(self):
        with patch('os.walk', return_value=[('.', [], [])]):
            result = searchFilesWithIds(['IHS-2005-0004', 'CRB-2009-0003'])
            self.assertEqual(result, [])

    def test_searchFilesWithIds_single(self):
        with patch('os.walk', return_value=[('.', [], ['IHS-2005-0004'])]):
            result = searchFilesWithIds(['IHS-2005-0004'])
            self.assertEqual(result, ['./IHS-2005-0004'])

    def test_searchFilesWithIds(self):
        with patch('os.walk', return_value=[('.', [], ['IHS-2005-0004', 'CRB-2009-0003'])]):
            result = searchFilesWithIds(['IHS-2005-0004', 'CRB-2009-0003'])
            self.assertEqual(result, ['./IHS-2005-0004', './CRB-2009-0003'])

if __name__ == '__main__':
    unittest.main()