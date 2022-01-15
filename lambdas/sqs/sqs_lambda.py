import os
import boto3


def handler(_, __):
    sqs = boto3.resource("sqs")
    queue = sqs.Queue(os.environ["QUEUE_URL"])
    params = {
        "MessageBody": "Message From Lambda",
    }
    queue.send_message(**params)
    return {"statusCode": 200}
