import boto3
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Questions')

    question_id = event['queryStringParameters']['id']
    user_id = json.loads(event['body'])['userId']

    # Fetch the current question
    response = table.get_item(Key={'question_id': question_id})
    question = response.get('Item')

    if not question:
        return {'statusCode': 404, 'body': json.dumps('Question not found')}

    upvotes = set(question.get('upvote', []))
    downvotes = set(question.get('downvote', []))

    if user_id in downvotes:
        return {'statusCode': 400, 'body': json.dumps('You have already downvoted')}
    
    if user_id in upvotes:
        upvotes.remove(user_id)
        downvotes.add(user_id)
        # Update the question
        table.update_item(
            Key={'question_id': question_id},
            UpdateExpression='SET upvote = :u, downvote = :d',
            ExpressionAttributeValues={
                ':u': list(upvotes),
                ':d': list(downvotes)
            }
        )
        return {'statusCode': 200, 'body': json.dumps('Response updated successfully')}
    
    # Add downvote
    downvotes.add(user_id)
    table.update_item(
        Key={'question_id': question_id},
        UpdateExpression='SET downvote = :d',
        ExpressionAttributeValues={
            ':d': list(downvotes)
        }
    )
    headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',  # Allows all domains, adjust if needed for security
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization'
    }


    return {'statusCode': 200, 'headers':headers, 'body': json.dumps('Downvoted successfully')}
