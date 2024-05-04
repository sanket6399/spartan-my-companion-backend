def lambda_handler(event, context):
    print("Disconnect:", event)
    return {'statusCode': 200}
