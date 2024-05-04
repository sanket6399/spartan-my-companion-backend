import json
import boto3
import uuid
from botocore.exceptions import ClientError
from datetime import datetime


# Initialize a DynamoDB client
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Parse incoming event
    print(event)
    print(event['body'])
    body_dict = json.loads(event.get('body', '{}'))
    question_id = event['queryStringParameters']['id']
    answer = body_dict.get('answer')
    user_id = body_dict.get('userId')
    # user_id = event['body'][1]
    # answer = event['body'][2]
    print(answer)
    
    # Table names
    replies_table = dynamodb.Table('Replies')
    questions_table = dynamodb.Table('Questions')

    # Create a new reply
    reply_id = str(uuid.uuid4())
    headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',  # Allows all domains, adjust if needed for security
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization'
        }
    try:
        reply = replies_table.put_item(
            Item={
                '_id': reply_id,
                'reply': answer,
                'author': user_id,
                "createdAt": datetime.now().isoformat(),
                "updatedAt": datetime.now().isoformat(),
                "__v": 0
            }
        )
    except ClientError as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error in creating reply'})
        }

    # Link reply to the question
    try:
        update_response = questions_table.update_item(
            Key={'question_id': question_id},
            UpdateExpression='SET replies = list_append(replies, :val)',
            ExpressionAttributeValues={
                ':val': [reply_id]
            }
        )
    except ClientError as e:
        print(e)
        return {
            
            'statusCode': 500,
            'headers':headers,
            'body': json.dumps({'message': 'Error in updating question with reply'})
        }

    # Return success response
    return {
        'statusCode': 201,
        'headers':headers,
        'body': json.dumps({'reply_id': reply_id, 'reply': answer, 'author': user_id})
    }
