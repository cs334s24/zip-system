import os
import shutil as sh
from flask import Flask, render_template, request
from zip import download_from_s3, zipSampleData, putZipToS3
from sendEmail import sendEmail

app = Flask(__name__)
tooBig = False  

def process_file_ids(file_ids, name_id):
    file_ids = file_ids.replace(" ", "")
    if len(name_id) == 0:
        name_id = '_'.join(file_ids.split(','))  # Join all file IDs if name_id is not provided
    if os.path.exists("temp-data"):
        sh.rmtree('temp-data')
    tooBig = False  # Reset tooBig before processing file_ids
    for file_id in file_ids.split(','):
        if download_from_s3(file_id):
            tooBig = True  # Set tooBig to True if any file exceeds the size limit
    if not tooBig:
        zipSampleData(name_id, file_ids.split(','))  # Zip the downloaded files before deleting the temp-data directory
        print(name_id+".zip has been created")
        putZipToS3(name_id+'.zip')
        os.remove(name_id+'.zip')
        sh.rmtree('temp-data')  # Delete the temp-data directory after zipping

@app.route('/')
def index():
    return render_template('index.html')

# Handling the form submission
@app.route('/docket-id', methods=['POST'])
def handle_form_submission():
    # Process the form submission
    docket_id = request.form['docket_id']
    name_id = request.form['name_id']
    email_id = request.form['email_id']
    process_file_ids(docket_id, name_id)
    print(name_id+'.zip')
    email_status = ""
    if email_id == None or email_id == "" or email_id == " ":
        email_status = f"No email provided!"
    else:
        try:
            sendEmail(email_id, docket_id)
            email_status = "Email sent successfully!"
        except Exception as e:
            print(f"An error occurred while sending email: {e}")
            email_status = f"Failed to send email: {e}"
    # Return some response to the client
    if tooBig:
        return f'Download too big!'
    else:
        return f'Docket ID: {docket_id}, Email Status: {email_status}'

if __name__ == "__main__":
    app.run(debug=True, port=8080)
