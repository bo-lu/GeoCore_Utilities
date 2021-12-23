import boto3

from botocore.exceptions import ClientError

""" A very simple DynamoDB wrapper written in python for AWS Lambda
"""

class Dynamodb:
    def __init__(self, region):
        #assuming aws secrets are know since we are running in lambda
        self._region = region
        self._dynamodb = boto3.resource('dynamodb', region_name=region)
        
    def create_table (self, table_name, schema, attributes, throughput=None, billing=None, gsi=None): 
        """Create a table and wait for completion
        """
        try:
            if throughput:
                if(len(gsi)>0):
                    table = self._dynamodb.create_table(
                        TableName=table_name,
                        KeySchema=schema,
                        AttributeDefinitions=attributes,
                        GlobalSecondaryIndexes=gsi,
                        ProvisionedThroughput=throughput
                    )
                else:
                    table = self._dynamodb.create_table(
                        TableName=table_name,
                        KeySchema=schema,
                        AttributeDefinitions=attributes,
                        ProvisionedThroughput=throughput
                    )
            elif billing:
                if(len(gsi)>0):
                    table = self._dynamodb.create_table(
                        TableName=table_name,
                        KeySchema=schema,
                        AttributeDefinitions=attributes,
                        GlobalSecondaryIndexes=gsi,
                        BillingMode=billing
                    )
                else:
                    table = self._dynamodb.create_table(
                        TableName=table_name,
                        KeySchema=schema,
                        AttributeDefinitions=attributes,
                        BillingMode=billing
                    )
            #wait for table completion
            table.meta.client.get_waiter('table_exists').wait(TableName=table)
        except ClientError as e:
            print(table, "table could NOT be created.")
            return False
        else:
            return True

    def create_item(self, table_name, item):
        """Create an item (dict) in table_name
        """
        try:
            table = self._dynamodb.Table(table_name)
            response = table.put_item(Item=item)
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return True
    
    def read_item(self, table_name, key):
        """Read an item by key
        """
        try:
            table = self._dynamodb.Table(table_name)
            response = table.get_item(Key=key)
            item = response.get('Item')
            if item is not None:
                return item
            else:
                return ItemNotFound(table_name, key)
        except ClientError as e:
            print(e.response['Error']['Message'])
            return False
        else:
            return True
            
    def query_item(self, table_name, expression, gsi=None):
        """Query for item by expression and gsi
        """
        try:
            table = self._dynamodb.Table(table_name)
            if gsi != None:
                response = table.query(
                    IndexName=gsi,
                    KeyConditionExpression=expression
                )
            else:
                response = table.query(
                    KeyConditionExpression=expression
                )
            return response.get('Items')
        except ClientError as e:
            print(e.response['Error']['Message'])
            return False
        else:
            return True
            
    def update_item(self, table_name, key,
                    attributes_to_update, operation="UPDATE_EXISTING_ATTRIBUTE_OR_ADD_NEW_ATTRIBUTE"):
        pass
    
    def delete_table (self, table_name):
        """Delete a table and wait for completion
        """
        try:
            table = self._dynamodb.Table(table_name)
            table.delete()
            #wait for table delete completion
            table.meta.client.get_waiter('table_not_exists').wait(TableName=table_name)
        except ClientError as e:
            print(table, "table could NOT be deleted:", e.response['Error']['Message'])
            return False
        else:
            return True
