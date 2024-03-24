import os
import boto3
import requests
from flask import Flask, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get user input
        downloadable_url = request.form['downloadable_url']
        access_key = request.form['access_key']
        secret_key = request.form['secret_key']
        endpoint_url = request.form['endpoint_url']
        bucket_name = request.form['bucket_name']
        file_name = request.form['file_name']

        # Download the file
        response = requests.get(downloadable_url)
        file_path = file_name
        with open(file_path, 'wb') as file:
            file.write(response.content)

        # Upload the file to S3
        s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key, endpoint_url=endpoint_url)
        s3.upload_file(file_path, bucket_name, file_name)

        # Delete the file from the VM
        os.remove(file_path)

        return redirect(url_for('success'))

    return '''
        <form method="post">
            <label for="downloadable_url">Downloadable URL:</label>
            <input type="text" id="downloadable_url" name="downloadable_url" required><br>

            <label for="access_key">Access Key:</label>
            <input type="text" id="access_key" name="access_key" required><br>

            <label for="secret_key">Secret Access Key:</label>
            <input type="text" id="secret_key" name="secret_key" required><br>

            <label for="endpoint_url">Endpoint URL:</label>
            <input type="text" id="endpoint_url" name="endpoint_url" required><br>

            <label for="bucket_name">Bucket Name:</label>
            <input type="text" id="bucket_name" name="bucket_name" required><br>

            <label for="file_name">File Name:</label>
            <input type="text" id="file_name" name="file_name" required><br>

            <input type="submit" value="Upload">
        </form>
    '''

@app.route('/success')
def success():
    return 'File uploaded successfully!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
