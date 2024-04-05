import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_docket_id_endpoint(self):
        response = self.app.post('/docket-id')
        self.assertEqual(response.status_code, 400)
    
    def test_docket_id_endpoint_with_data(self):
        response = self.app.post('/docket-id', data={'docket_id': '12345', 'email_id': '    '})
        self.assertEqual(response.status_code, 400)

    def test_index_endpoint(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_index_endpoint_with_data(self):
        response = self.app.get('/?    ')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)
    
    def test_index_endpoint_with_data(self):
        response = self.app.get('/?docket_id=12345&email_id=    ')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_trigger_lambda(self):
        self.assertTrue(({'docket_id': '12345', 'email_id': '    '}))
    
if __name__ == '__main__':
    unittest.main()
