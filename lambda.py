
import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    key = event["s3_key"]
    bucket = event["s3_bucket"]
    
    boto3.resource('s3').Bucket(bucket).download_file(key, "/tmp/image.png")
    
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }


import os
import io
import boto3
import json
import base64

ENDPOINT_NAME = 'image-classification-2021-12-04-07-33-27-658'
runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    
    image = base64.b64decode(event["image_data"])
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='image/png',
                                       Body=image)
    
    event["inferences"] = json.loads(response['Body'].read().decode('utf-8'))
    return {
        'statusCode': 200,
        'body': event
    }



import json


THRESHOLD = .97

def lambda_handler(event, context):
    inferences = event["inferences"]
    
    meets_threshold = (max(inferences) > THRESHOLD)
    
    if meets_threshold:
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': event
    }