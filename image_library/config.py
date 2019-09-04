import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    PHOTOS_PER_PAGE = os.environ.get('PHOTOS_PER_PAGE')
    # S3 variables
    S3_REGION = os.environ.get("S3_REGION")
    S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
    S3_ACCESS_KEY = os.environ.get("S3_ACCESS_KEY")
    S3_SECRET_ACCESS_KEY = os.environ.get("S3_SECRET_ACCESS_KEY")
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET_NAME)
    # S3 -> to Save image on AWS S3
    SAVE_IMAGE_LOCAL = os.environ.get("SAVE_IMAGE_LOCAL")
    # Data Base Local
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    # Data Base MongoDB
    MONGODB_DATABASE_URI = os.environ.get('MONGODB_DATABASE_URI')
