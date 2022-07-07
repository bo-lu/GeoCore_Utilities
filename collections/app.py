import os
import io
import json
import boto3
import requests
import logging
import pandas as pd
import awswrangler as wr

from uuid import UUID
from botocore.exceptions import ClientError

PARQUET_BUCKET_NAME = os.environ['PARQUET_BUCKET_NAME']

def lambda_handler(event, context):
    
    """ 
    Parse query string parameters 
    """
    
    try:
        uuid = event["id"]
    except:
        uuid = False
    
    message = ""
    if uuid != False:
        try:
            print("Finding the parent and other children for uuid: ", uuid)
            geocore_df = wr.s3.read_parquet(path=PARQUET_BUCKET_NAME)
        except ClientError as e:
            message += "Error accessing " + PARQUET_BUCKET_NAME
            return {
                'statusCode': 200,
                'body': json.dumps(message)
            }
        
        self_json = find_self(geocore_df, uuid)
        
        parent_json, parent_id  = find_parent(geocore_df, uuid)
        
        child_json, child_count  = find_children(geocore_df, parent_id, uuid)

    else:
        message += "No id parameter was passed. Usage: ?id=XYZ"
        return {
            'statusCode': 200,
            'body': message
        }
    
    return {
        'statusCode': 200,
        'sibling_count': child_count,
        'self': self_json,
        'parent': parent_json,
        'sibling': child_json
    }

def find_self(geocore_df, uuid):
    """
    Find uuid if it exists
    :param geocore_df: dataframe containing all geocore records
    :param uuid: unique id we are looking up 
    :return message: JSON of the uuid and record title in english and french
    """
    
    self_desc_en = ""
    self_desc_fr = ""
    self_df = geocore_df[geocore_df['features_properties_id'] == uuid]

    if len(self_df) == 0:
        self_message = None
    else:
        try:
            self_desc_en = self_df.iloc[0]['features_properties_title_en']
            self_desc_fr = self_df.iloc[0]['features_properties_title_fr']
            self_message = '{ "id": "' + uuid + '", "description_en": "' + self_desc_en + '", "description_fr": "' + self_desc_fr + '"}'
        except:
            self_message = None

    return nonesafe_loads(self_message)
    
def find_parent(geocore_df, uuid):
    """
    Find parent record of a uuid if it exists
    :param geocore_df: dataframe containing all geocore records
    :param uuid: unique id we are looking up 
    :return message: JSON of the uuid and record title in english and french
    :return parent_id: uuid of the parent record
    """
    parent_id = ""
    parent_desc_en = ""
    parent_desc_fr = ""
    parent_df = geocore_df[geocore_df['features_properties_id'] == uuid]

    if len(parent_df) == 0:
        parent_message = None
    else:
        try:
            parent_id = parent_df.iloc[0]['features_properties_parentIdentifier']
            parent_desc_en = geocore_df[geocore_df['features_properties_id'] == parent_id].iloc[0]['features_properties_title_en']
            parent_desc_fr = geocore_df[geocore_df['features_properties_id'] == parent_id].iloc[0]['features_properties_title_fr']
            parent_message = '{ "id": "' + parent_id + '", "description_en": "' + parent_desc_en + '", "description_fr": "' + parent_desc_fr + '"}'
        except:
            parent_message = None
            parent_id = uuid

    return nonesafe_loads(parent_message), parent_id

def find_children(geocore_df, parent_id, uuid):
    """
    Find sibling records of a uuid if it exists
    :param geocore_df: dataframe containing all geocore records
    :param uuid: unique id we are looking up
    :return message: JSON of the uuid and record title in english and french
    :return parent_id: uuid of the parent record
    """
    child_array_id = []
    child_array_desc_en = []
    child_array_desc_fr = []
    other_children_df = geocore_df[geocore_df['features_properties_parentIdentifier'] == parent_id]
    
    #cannot be its own sibling. remove self from the siblings dataframe
    other_children_df = other_children_df[other_children_df['features_properties_id'] != uuid]
    
    if len(other_children_df) == 0:
        child_message = None
    else:
        child_message = "["
        for i in range(0,len(other_children_df)):
            child_array_id.append(other_children_df.iloc[i]['features_properties_id'])
            child_array_desc_en.append(other_children_df.iloc[i]['features_properties_title_en'])
            child_array_desc_fr.append(other_children_df.iloc[i]['features_properties_title_fr'])

        for i in range(0,len(other_children_df)):
            child_message += '{ "id": "' + child_array_id[i] + '", "description_en": "' + child_array_desc_en[i] + '", "description_fr": "' + child_array_desc_fr[i] + '"}'
            if i != len(other_children_df)-1:
                child_message += ', '
        child_message += "]"
    
    return nonesafe_loads(child_message), len(other_children_df)
    
def nonesafe_loads(obj):
    if obj is not None:
        return json.loads(obj)
