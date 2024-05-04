import json
import boto3

def get_dynamodb_client():
    return boto3.client('dynamodb', region_name='us-east-1')

def lambda_handler(event, context):
    dynamodb = get_dynamodb_client()

    # Process each message
    for record in event['Records']:
        body = json.loads(record['body'])
        question_id, question, description, author, tags = body['question_id'], body['question'], body['description'], body['author'], body['tags']
        updated_time, created_time = body['updatedAt'], body['createdAt']

        response = dynamodb.put_item(
            TableName='Questions',
            Item={
                'question_id': {'S': question_id},
                'question': {'S': question},
                'description': {'S': description},
                'author': {'S': author},
                'tags': {'SS': tags},
                'replies': {'L': []},
                'upvote': {'L': []},
                'downvote': {'L': []},
                'updatedAt': {'S': updated_time},
                'createdAt' : {'S':created_time}
            }
        )
    return {'statusCode': 200, 'body': {'message': 'Question inserted into DynamoDB'}}
