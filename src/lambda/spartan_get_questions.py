import json
import boto3
import logging

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_dynamodb_resource():
    return boto3.resource('dynamodb', region_name='us-east-1')

# Initialize a DynamoDB resource
dynamodb = get_dynamodb_resource()

def convert_sets_to_lists(data):
    """Recursively converts sets to lists in given data."""
    if isinstance(data, set):
        return list(data)
    elif isinstance(data, list):
        return [convert_sets_to_lists(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_sets_to_lists(value) for key, value in data.items()}
    else:
        return data

def lambda_handler(event, context):
    try:
        # Assuming 'Questions' is your table name
        table = dynamodb.Table('Questions')
        
        # Scan operation to fetch all questions
        response = table.scan()
        
        questions = response['Items']
        questions = sorted(questions, key=lambda x: x.get('createdAt', ''), reverse=True)

        for question in questions:
            if 'replies' in question:
                replies = []
                reply_table = dynamodb.Table('Replies')
                for reply_id in question['replies']:
                    reply = reply_table.get_item(Key={'_id': reply_id}).get('Item')
                    if reply and 'author' in reply:
                        author_table = dynamodb.Table('Users')
                        author = author_table.get_item(Key={'_id': reply['author']}).get('Item')
                        reply['author'] = author
                    replies.append(reply)
                question['replies'] = replies
            
            if 'author' in question:
                author_table = dynamodb.Table('Users')
                author = author_table.get_item(Key={'_id': question['author']}).get('Item')
                logger.info(f"Questions {question}")
                question['author'] = author
            if 'tags' in question and isinstance(question['tags'], set):
                question['tags'] = list(question['tags'])



        logger.info(f"Questions: {questions}")
        # Return the result as a JSON
        return {
            'statusCode': 200,
            'body': questions
        }
    except Exception as e:
        logger.error("Error processing request", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Server Error', 'error': str(e)})
        }
