import boto3
import os
from werkzeug.utils import secure_filename

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

s3 = boto3.client('s3', 
                  aws_access_key_id=AWS_ACCESS_KEY_ID, 
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def upload_file_to_s3(file):
    filename = secure_filename(file.filename)
    file_path = os.path.join('/tmp', filename)
    file.save(file_path)
    s3.upload_file(file_path, S3_BUCKET_NAME, filename)
    s3_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{filename}"
    return s3_url