import json
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime

# Initialize a DynamoDB client
# dynamodb = boto3.resource('dynamodb')
def get_dynamodb_client():
    return boto3.resource('dynamodb', region_name='us-east-1')

def lambda_handler(event, context):
    print(event)
    dynamodb = get_dynamodb_client()
    table = dynamodb.Table('Users')

    # Scan the table - note: consider using Query if the dataset is large
    response = table.scan()
    print(response)
    # Process records to conform to the specified format
    users = []
    for item in response['Items']:
        user = {
            "_id": item['_id'],
            "name": item['name'],
            "profileImage": item['profileImage'],
            "email": item['email'],
            "password": item['password'],
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat(),
            "__v": 0
        }
        users.append(user)

    # Return the formatted data
    return {
        'statusCode': 200,
        'body': users,
        'headers': {
            'Content-Type': 'application/json'
        }
    }
