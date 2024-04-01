import unittest
from unittest.mock import patch
from sendEmail import sendEmail

class TestSendEmail(unittest.TestCase):
    """Test cases for sendEmail function."""

    @patch('smtplib.SMTP')
    def test_send_email_success(self, mock_smtp):
        """Test sendEmail function for successful email sending."""
        to_email = 'regulations_data@moravian.edu' 
        docket_id = 'CRB-2009-0003'
        result = sendEmail(to_email, docket_id)
        self.assertEqual(result, "Email sent successfully!")

    @patch('smtplib.SMTP')
    def test_send_email_failure(self, mock_smtp):
        """Test sendEmail function for failure in email sending."""
        to_email = 'regulations_data@moravian.edu'
        docket_id = 'CRB-2009-0003'
        mock_smtp.side_effect = Exception('SMTP Connection Error')
        result = sendEmail(to_email, docket_id)
        self.assertIn("Failed to send email:", result)

    def test_send_email_no_email(self):
        """Test sendEmail function when email is not provided."""
        to_email = ''
        docket_id = 'CRB-2009-0003'
        result = sendEmail(to_email, docket_id)
        self.assertIn("Failed to send email:", result)
    
    def test_send_email_no_docket_id(self):
        """Test sendEmail function when docket ID is not provided."""
        to_email = 'regulations_data@moravian.edu' 
        docket_id = ''
        result = sendEmail(to_email, docket_id)
        self.assertIn("Failed to send email:", result)

    def test_send_email_no_email_no_docket_id(self):
        """Test sendEmail function when neither email nor docket ID is provided."""
        to_email = ''
        docket_id = ''
        result = sendEmail(to_email, docket_id)
        self.assertIn("Failed to send email:", result)

if __name__ == '__main__':
    unittest.main()
