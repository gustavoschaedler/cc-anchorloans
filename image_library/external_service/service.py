import boto3
import botocore
from image_library.config import Config

s3 = boto3.client(
    's3',
    region_name=Config.S3_REGION,
    aws_access_key_id=Config.S3_ACCESS_KEY,
    aws_secret_access_key=Config.S3_SECRET_ACCESS_KEY
)


def upload_file_to_s3(file, path, bucket_name=Config.S3_BUCKET_NAME, acl='public-read'):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            path + '/' + file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        return "Erro on upload file to AWS S3: " + e

    return "{}{}/{}".format(Config.S3_LOCATION, path, file.filename)
