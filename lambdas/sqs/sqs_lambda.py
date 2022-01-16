import os
import json
import boto3


def handler(_, __):
    sqs = boto3.resource("sqs")
    queue = sqs.Queue(os.environ["QUEUE_URL"])
    params = {
        "MessageBody": "Message From Lambda",
    }
    queue.send_message(**params)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": "Message sent to SQS"}),
    }
