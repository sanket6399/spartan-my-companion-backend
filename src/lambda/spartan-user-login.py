import boto3
import json

def get_dynamodb_client():
    return boto3.client('dynamodb', region_name='us-east-1')

def lambda_handler(event, context):
    dynamodb = get_dynamodb_client()
    print(event)
    body = event  # Assuming the body is JSON encoded string
    
    email = body['email']
    password = body['password']

    # Find user by email using get_item
    try:
        response = dynamodb.scan(
            TableName='Users',
            FilterExpression='email = :email',
            ExpressionAttributeValues={
                ':email': {'S': email}
            }
        )
        print(response)
        user = response.get('Items', None)
        if not user:
            return {'statusCode': 400, 'body': json.dumps({'message': 'User does not exist'})}

        # Check password
        if user[0]['password']['S'] == password:
            # Remove sensitive data before returning
            user[0].pop('password', None)
            data = user

            # Convert the DynamoDB format to a standard JSON dictionary
            converted_data = {
                "_id": data[0]["_id"]["S"],
                "email": data[0]["email"]["S"],
                "name": data[0]["name"]["S"],
                "profileImage": data[0]["profileImage"]["S"]
            }
            return {'statusCode': 200, 'body': converted_data}
        else:
            return {'statusCode': 400, 'body': json.dumps({'message': 'Incorrect password'})}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'message': str(e)})}

