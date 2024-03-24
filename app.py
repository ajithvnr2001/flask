import os
import boto3
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def download_file(url, file_path):
    response = requests.get(url)
    with open(file_path, 'wb') as file:
        file.write(response.content)

def upload_to_s3(file_path, bucket_name, object_key, endpoint_url):
    s3 = boto3.client('s3', endpoint_url=endpoint_url)
    s3.upload_file(file_path, bucket_name, object_key)

def delete_file(file_path):
    os.remove(file_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        bucket_name = request.form['bucket_name']
        access_key = request.form['access_key']
        secret_key = request.form['secret_key']
        endpoint_url = request.form['endpoint_url']
        file_name = request.form['file_name']

        file_path = file_name

        # Download the file
        download_file(url, file_path)

        # Configure AWS credentials
        os.environ['AWS_ACCESS_KEY_ID'] = access_key
        os.environ['AWS_SECRET_ACCESS_KEY'] = secret_key

        # Upload the file to S3
        upload_to_s3(file_path, bucket_name, file_name, endpoint_url)

        # Delete the file from Vercel server
        delete_file(file_path)

        return redirect(url_for('success'))

    return render_template('index.html')

@app.route('/success')
def success():
    return "File downloaded, uploaded to S3, and deleted from Vercel server."

if __name__ == '__main__':
    app.run()
