# app.py
import os
import shutil as sh
from flask import Flask, render_template, request
from zip import download_from_s3, zipSampleData

def process_file_ids(file_ids):
    if os.path.exists("temp-data"):
        sh.rmtree('temp-data')
    for file_id in file_ids:
        print(file_id)
        download_from_s3(file_id)  # Call functions from the imported zip module
    zipSampleData()  # Call functions from the imported zip module
    print("data.zip has been created")
    sh.rmtree('temp-data')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Handling the form submission
@app.route('/docket-id', methods=['POST'])
def handle_form_submission():
    # Get the 'docket-id' from the form data
    docket_id = request.form['docket-id']
    
    # Pass the 'docket-id' to another function
    result = process_file_ids(docket_id)
    
    # Return some response to the client
    return 'Docket ID: {}'.format(result)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
