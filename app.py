import os
import shutil as sh
from flask import Flask, render_template, request
from zip import download_from_s3, zipSampleData
from sendEmail import sendEmail

def process_file_ids(file_ids):
    if os.path.exists("temp-data"):
        sh.rmtree('temp-data')
    for file_id in file_ids:
        print(file_id)
        download_from_s3(file_id)
    zipSampleData()
    print("data.zip has been created")
    sh.rmtree('temp-data')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Handling the form submission
@app.route('/docket-id', methods=['POST'])
def handle_form_submission():
    # Process the form submission
    docket_id = request.form['docket_id']
    process_file_ids([docket_id])
    email_status = ""
    try:
        email_id = request.form['email_id']
        sendEmail(email_id, docket_id)
        email_status = "Email sent successfully!"
    except Exception as e:
        print(f"An error occurred while sending email: {e}")
        email_status = f"Failed to send email: {e}"
    # Return some response to the client
    return f'Docket ID: {docket_id}, Email Status: {email_status}'

if __name__ == "__main__":
    app.run(debug=True, port=8080)
