import boto3

def getTextFromS3(S3_BUCKET, S3_KEY):
    s3 = boto3.resource('s3')

    obj = s3.Object(S3_BUCKET, S3_KEY)
    reminder_text = obj.get()['Body'].read().decode('utf-8')

    return reminder_text

def splitTextIntoListOfSSML(reminder_text):

    # remove empty strings
    reminder_list = filter(len, reminder_text.split('\n'))

    # remove non-speakable chars
    #reminder_list_alnum = [x.translate(None, '[]$()<>\'"') for x in reminder_list]

    parsedText = '. <break time="3s"/>'.join(reminder_list)

    ssml = "<speak>" + parsedText + "</speak>"

    return ssml



