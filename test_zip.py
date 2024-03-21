import unittest
import shutil
from unittest.mock import patch, Mock
import os
from zip import (
    getFileIdsFromUser,
    searchFilesWithIds,
    zipSampleData,
    putZipToS3,
    download_from_s3,
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
        
    @patch('sh.aws')
    @patch('os.mkdir')
    def test_download_from_s3(self, mocked_mkdir, mocked_aws):
        download_from_s3('IHS-2005-0004')
        mocked_mkdir.assert_called()
        mocked_aws.assert_called_once_with('s3', 'cp', 's3://mirrulations-sample-data-opensearch/IHS/IHS-2005-0004', 'temp-data/data/IHS-2005-0004', '--recursive')

    def test_download_from_s3_exists(self):
        os.mkdir('temp-data')
        os.mkdir('temp-data/data')
        download_from_s3('IHS-2005-0004')
        self.assertTrue(os.path.exists('temp-data/data/IHS-2005-0004'))
        shutil.rmtree('temp-data')

    def test_zipSampleData(self):
        os.mkdir('temp-data')
        os.mkdir('temp-data/data')
        os.mkdir('temp-data/data/IHS-2005-0004')
        with open('temp-data/data/IHS-2005-0004/test.txt', 'w') as f:
            f.write('test')
        zipSampleData()
        self.assertTrue(os.path.exists('data.zip'))
        os.remove('data.zip')
        shutil.rmtree('temp-data')

    def test_zipSampleData_no_temp_data(self):
        zipSampleData()
        self.assertTrue(os.path.exists('data.zip'))
        os.remove('data.zip')

    def test_zipSampleData_no_temp_data_data(self):
        os.mkdir('temp-data')
        zipSampleData()
        self.assertTrue(os.path.exists('data.zip'))
        os.remove('data.zip')
        shutil.rmtree('temp-data')

if __name__ == '__main__':
    unittest.main()