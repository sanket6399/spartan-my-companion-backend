import json
import boto3
from boto3.dynamodb.conditions import Attr

# Initialize a DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def lambda_handler(event, context):
    print(event)
    user_id = event['queryStringParameters']['id']
    table = dynamodb.Table('Questions')  # Use the correct table name

    try:
        # Scanning the table with a filter expression for author
        response = table.scan(
            FilterExpression=Attr('author').eq(user_id)
        )

        questions = [
            {
                "question_id": item['question_id'],
                "author": item['author'],
                "description": item['description'],
                "question": item['question'],
                "tags": list(item['tags']),
                "replies": item.get('replies', []),
                "upvote": len(item.get('upvote', [])),
                "downvote": len(item.get('downvote', []))
            }
            for item in response['Items']
        ]
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',  # Allows all domains, adjust if needed for security
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization'
        }
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(questions)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal Server Error 2'})
        }
