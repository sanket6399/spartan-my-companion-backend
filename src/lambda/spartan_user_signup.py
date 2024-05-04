import boto3
import json
import uuid
def get_dynamodb_client():
    return boto3.client('dynamodb', region_name='us-east-1')

def lambda_handler(event, context):
    print(event)
    dynamodb = get_dynamodb_client()
    
    body = event
    
    # Extract details from the parsed JSON body
    name = body['name']
    password = body['password']
    email = body['email']
    profile_image = body.get('profileImage', 'default_image_url')  # Provide a default if not present

    # Check if user already exists using GetItem
    try:
        response = dynamodb.scan(
            TableName='Users',
            FilterExpression='email = :email',
            ExpressionAttributeValues={
                ':email': {'S': email}
            }
        )

        if response['Items']:
            return {'statusCode': 400, 'body': json.dumps({'message': 'Email already exists'})}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'message': str(e)})}

    # Insert new user
    try:
        user_id = str(uuid.uuid4())
        response = dynamodb.put_item(
            TableName='Users',
            Item={
                '_id' : {'S': user_id},
                'name': {'S': name},
                'email': {'S': email},
                'password': {'S': password},
                'profileImage': {'S': profile_image}
            }
        )
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'User created successfully',
                'userInfo': {
                    '_id': user_id,
                    'name': name,
                    'email': email,
                    'profileImage': profile_image
                }
            })
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'message': str(e)})}

