from flask import Flask, render_template, request
import boto3
import json

app = Flask(__name__)

LOCAL_TESTING = False

@app.route('/')
def index():
    return render_template('system.html')

@app.route('/docket-id', methods=['POST'])
def process_list():
    docket_id = request.form['docket_id']
    email_id = request.form['email_id']
    data = {'docket_id': docket_id, 'email_id': email_id}

    result = trigger_lambda(data)

    if result:
        return 'Lambda function triggered successfully!', 200
    else:
        return 'Failed to trigger Lambda function!', 500

def trigger_lambda(data):
    if LOCAL_TESTING:
        # Stub or mock function for local testing
        print("Mocking Lambda invocation with data:", data)
        return 'Mocked Lambda invocation successful!'
    else:
        # Invoke real Lambda function using Boto3
        lambda_client = boto3.client('lambda', region_name='us-east-1')
        response = lambda_client.invoke(
            FunctionName='ZipSystemLambda',
            InvocationType='Event',
            Payload=json.dumps(data)
        )
        return response['StatusCode'] == 200

if __name__ == '__main__':
    app.run(port=8080)