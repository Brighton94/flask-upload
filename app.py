from flask import Flask, render_template, request
import boto3
from boto3.s3.transfer import TransferConfig
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv("credentials.env")

app = Flask(__name__)

session = boto3.session.Session()
client = session.client('s3',
                    region_name=os.getenv('SPACES_REGION_NAME'),
                    endpoint_url=os.getenv('SPACES_ENDPOINT_URL'),
                    aws_access_key_id=os.getenv('ACCESS_KEY'),
                    aws_secret_access_key=os.getenv('SECRET_KEY'))

@app.route('/')  
def home():
    return render_template("file_upload_to_s3.html")

@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
                filename = secure_filename(file.filename)
                file.save(filename)
                MB = 1024 ** 2
                conf = TransferConfig(multipart_threshold=1*MB, max_io_queue=10**3, multipart_chunksize=1*MB, max_concurrency=500)
                client.upload_file(
                    Bucket = os.getenv('SPACES_NAME'),
                    Filename=filename,
                    Key = filename,
                    Config = conf
                )
                msg = "Upload Done ! "

    return render_template("file_upload_to_s3.html",msg =msg)


if __name__ == "__main__":
    
    app.run(debug=True)