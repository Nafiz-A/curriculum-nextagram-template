import boto3
import botocore
from app import app
from config import S3_KEY, S3_SECRET, S3_BUCKET, Config

s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)


def upload_file_to_s3(file, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            S3_BUCKET,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}".format(app.config["S3_LOCATION"], file.filename)
