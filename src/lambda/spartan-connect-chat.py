import boto3
import json

def lambda_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ChatMessages')

    if event['requestContext']['eventType'] == 'CONNECT':
        # Add the new connection to the Users table
        table.put_item(Item={'ConnectionId': str(connection_id)})
        return {'statusCode': 200}
    
    elif event['requestContext']['eventType'] == 'DISCONNECT':
        # Remove the connection from the Users table
        table.delete_item(Key={'ConnectionId': str(connection_id)})
        return {'statusCode': 200}
