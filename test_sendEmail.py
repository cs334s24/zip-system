import unittest
from unittest.mock import patch
from sendEmail import sendEmail

class TestSendEmail(unittest.TestCase):
    @patch('smtplib.SMTP')
    def test_sendEmail_success(self, mock_smtp):
        # Mock environment variables
        with patch.dict('os.environ', {'EMAIL': 'your_email@gmail.com', 'PASSWORD': 'your_password'}):
            result = sendEmail('recipient@example.com', '123456')
        self.assertEqual(result, "Email sent successfully!")

    @patch('smtplib.SMTP')
    def test_sendEmail_failure(self, mock_smtp):
        # Mock environment variables
        with patch.dict('os.environ', {'EMAIL': 'your_email@gmail.com', 'PASSWORD': 'your_password'}):
            mock_smtp.side_effect = Exception('Mocked SMTP error')
            result = sendEmail('recipient@example.com', '123456')
        self.assertEqual(result, "Failed to send email: Mocked SMTP error")

    def test_sendEmail_no_credentials(self):
        # Missing EMAIL and PASSWORD environment variables
        result = sendEmail('recipient@example.com', '123456')
        self.assertIn("Failed to send email:", result)

if __name__ == '__main__':
    unittest.main()
