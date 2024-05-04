import boto3
import json

def lambda_handler(event, context):
    print(event)
    message = json.loads(event['body']).get('data')
    room = json.loads(event['body']).get('room')
    sender_id = json.loads(event['body']).get('senderId')
    dynamodb = boto3.resource('dynamodb')
    users_table = dynamodb.Table('ChatMessages')
    messages_table = dynamodb.Table('Messages')

    # Save message to DynamoDB
    messages_table.put_item(Item={
        'messageId': context.aws_request_id,  # Unique ID for the message
        'senderId': sender_id,
        'room': room,
        'message': message,
        'timestamp': str(event['requestContext']['requestTime'])
    })

    # Retrieve all connections
    response = users_table.scan()
    connections = [user['ConnectionId'] for user in response['Items']]

    # Send the message to all connected clients
    client = boto3.client('apigatewaymanagementapi', endpoint_url=f"https://{event['requestContext']['domainName']}/{event['requestContext']['stage']}")

    for connection_id in connections:
        try:
            client.post_to_connection(ConnectionId=connection_id, Data=json.dumps({'message': message, 'sender': sender_id}))
        except client.exceptions.GoneException:
            # Handle the case where the connection is no longer available
            users_table.delete_item(Key={'ConnectionId': connection_id})

    return {'statusCode': 200}
