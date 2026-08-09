import boto3 #official aws sdk for python
import os

from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

def list_bucket_files():

    response = s3_client.list_objects_v2(
        Bucket=BUCKET_NAME
    )

    return response


def upload_file(file, filename):

    """
    Upload a file to AWS S3 and store its metadata in PostgreSQL.
    """

    s3_client.upload_fileobj(
        file,
        BUCKET_NAME,
        filename
    )

    return filename


def generate_download_url(object_key):
    url = s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket":BUCKET_NAME,
            "Key":object_key
        },
        ExpiresIn= 300
    )
    return url

def delete_from_s3(object_key):

    s3_client.delete_object(
        Bucket=BUCKET_NAME,
        Key= object_key
    )