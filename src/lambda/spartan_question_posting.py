import json
import boto3
import uuid
from datetime import datetime, timedelta, timezone

def get_sqs_client():
    return boto3.client('sqs', region_name='us-east-1')

def get_pacific_time():
    utc_time = datetime.now(timezone.utc)
    # print(utc_time)
    pst_time = utc_time - timedelta(hours=7)
    # print(pst_time)
    return str(pst_time)

def lambda_handler(event, context):
    sqs = get_sqs_client()
    body = event
    question, description, author_id, tags = body['question'], body['description'], body['userId'], body['tags']
    questionid = str(uuid.uuid4())

    # Create message body
    message_body = {
        'question_id': questionid,
        'question': question,
        'description': description,
        'author': author_id,
        'tags': tags,
        'createdAt': get_pacific_time(),
        'updatedAt': get_pacific_time(),
    }

    # Send message to SQS
    response = sqs.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/730335579154/spartan-event',
        MessageBody=json.dumps(message_body)
    )
    return {'statusCode': 200, 'body': {'message': 'Message sent to SQS'}}
