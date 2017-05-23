import boto3


QUEUE_URL = 'YOUR_QUEUE_URL_HERE'
WORKER_FUNCTION_NAME = 'serverless-tq-sqs-worker'


def lambda_handler(event, context):
    lambda_client = boto3.client('lambda')

    # Read messages from SQS
    queue = boto3.resource('sqs').Queue(QUEUE_URL)
    messages = queue.receive_messages(MaxNumberOfMessages=10)

    # Invoke worker function for each message and delete it
    for message in messages:
        print message.body
        lambda_client.invoke_async(
            FunctionName=WORKER_FUNCTION_NAME, InvokeArgs=message.body)
        message.delete()

    return None
