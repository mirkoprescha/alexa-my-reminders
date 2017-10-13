import boto3
MAX_ALEXA_SPEACH_OUTPUT=8000


def getTextFromS3(S3_BUCKET, S3_KEY):
    s3 = boto3.resource('s3')

    obj = s3.Object(S3_BUCKET, S3_KEY)
    reminder_text = obj.get()['Body'].read().decode('utf-8')

    return reminder_text

def clean_text(reminder_text):

    # remove empty strings
    reminder_list = filter(len, reminder_text.split('\n'))


    # remove non-speakable chars
    #reminder_list_alnum = [x.translate(None, '[]$()<>\'"') for x in reminder_list]

    reminder_list_break = [x.strip().strip(".") + '.' for x in reminder_list]

    return reminder_list_break

def generate_ssml(reminder_text):
    import random
    # add point and break to each reminder
    reminder_list_with_break = [x + '<break time="3s"/>' for x in reminder_text]

    #remove until 8000 chars
    while sum(len(x) for x in reminder_list_with_break) > (MAX_ALEXA_SPEACH_OUTPUT - 1100):
        index_to_remove = random.randint(0,len(reminder_list_with_break)-1)
        print "remove element with index {} from reminder list, because speech out reached limit".format(index_to_remove)
        reminder_list_with_break.pop(index_to_remove)


    ssml = "<speak>" + ''.join(reminder_list_with_break) + "</speak>"
    print "length of ssml is " + str(len(ssml))

    return ssml



