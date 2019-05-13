from __future__ import print_function

import boto3
from decimal import Decimal
import json
import urllib

print('Loading function')

rekognition = boto3.client('rekognition')
client = boto3.client('sns')


def detect_labels(bucket, key):
    response = rekognition.detect_text(Image={"S3Object": {"Bucket": bucket, "Name": key}})
    return response


def lambda_handler(event, context):
    target_ARN = 'YOUR_ARN'
    bucket = "YOUR_BUCKET"
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    
    correct_number_plate = "YOUR_PLATE"
    

    try:
        response = detect_labels(bucket, key)
        #msg = str(bucket)+" "+str(key)
        textDetections = response['TextDetections']
        
        number_plate = ""
        
        for text in textDetections:
            if text['Type'] == 'LINE':
                if text['DetectedText'].isupper():
                    number_plate += text['DetectedText']
        
        number_plate = number_plate.strip().replace(" ","")
        
        if number_plate in correct_number_plate:
            pub = client.publish(TargetArn=target_ARN, Message="Opening gate for: "+number_plate, Subject='Gate recognition')
        else:
            pub = client.publish(TargetArn=target_ARN, Message="Someone waiting: "+number_plate, Subject='Gate recognition')


        return response
    except Exception as e:
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        pub = client.publish(TargetArn=target_ARN, Message=str(e), Subject='Gate recognition')

        raise e
