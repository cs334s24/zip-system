import unittest
from unittest.mock import patch
from sendEmail import sendEmail

class TestSendEmail(unittest.TestCase):
    @patch('smtplib.SMTP')
    def test_sendEmail_success(self, mock_smtp):
        to_email = 'Need to fill in a real email address here' # You will have to put in a real email address here
        docket_id = 'CRB-2009-0003'
        result = sendEmail(to_email, docket_id)
        self.assertEqual(result, "Email sent successfully!")

    @patch('smtplib.SMTP')
    def test_sendEmail_failure(self, mock_smtp):
        to_email = 'Need to fill in a real email address here' # You will have to put in a real email address here
        docket_id = 'CRB-2009-0003'
        mock_smtp.side_effect = Exception('SMTP Connection Error')
        result = sendEmail(to_email, docket_id)
        self.assertIn("Failed to send email:", result)

    def test_sendEmail_no_email(self):
        to_email = ''
        docket_id = 'CRB-2009-0003'
        result = sendEmail(to_email, docket_id)
        self.assertIn("Failed to send email:", result)
    
    def test_sendEmail_no_docket_id(self):
        to_email = 'Need to fill in a real email address here' # You will have to put in a real email address here
        docket_id = ''
        result = sendEmail(to_email, docket_id)
        self.assertIn("Failed to send email:", result)

    def test_sendEmail_no_email_no_docket_id(self):
        to_email = ''
        docket_id = ''
        result = sendEmail(to_email, docket_id)
        self.assertIn("Failed to send email:", result)

if __name__ == '__main__':
    unittest.main()
