import boto3
from config import S3_BUCKET, S3_KEY

def getTextFromS3():
    s3 = boto3.resource('s3')

    obj = s3.Object(S3_BUCKET, S3_KEY)
    reminder_text = obj.get()['Body'].read().decode('utf-8')

    return reminder_text

