import os
import io
import json
import requests
import logging

from botocore.exceptions import ClientError

import boto3

GEONETWORK_POPULARITY_PATH = os.environ['GEONETWORK_POPULARITY_PATH']

def lambda_handler(event, context):
    """
    AWS Lambda Entry
    """
    
    base_path = "https://maps.canada.ca/geonetwork/srv/eng/q?fast=index&buildSummary=false&_content_type=json&uuid="
    message = ""
    popularity = "0"
    uuid = "None"
    
    try:
        uuid = str(event["queryStringParameters"]["uuid"])
    except:
        message = "UUID was not supplied or is invalid"

    """debug"""
    #uuid = ["296de17c-001c-4435-8f9a-f5acab632e85"]
    """end debug"""
    
    response = requests.get(base_path + uuid)
    if response.ok:
        print(response)
        str_data = json.loads(response.text)
        popularity = str(str_data['metadata']['popularity'])
        message = "Success"
    else:
        message = "Could not access: " + base_path + uuid
    
    response = {
        "statusCode": "200",
        "headers": {"Content-type": "application/json"},
        "body": json.dumps(
            {
                "uuid": uuid,
                "popularity": popularity,
                "message": message,
            }
        ),
    }
    return response
