import os
import json
import boto3


def handler(_, __):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["TABLE_NAME"])
    params = {
        "Key": {"pkey": "counter"},
        "ReturnValues": "UPDATED_NEW",
        "UpdateExpression": "SET atomic_counter = if_not_exists(atomic_counter, :start) + :inc",
        "ExpressionAttributeValues": {
            ":inc": 1,
            ":start": 0,
        },
    }
    response = table.update_item(**params)
    counter = int(response["Attributes"]["atomic_counter"])
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"counter": counter}),
    }
