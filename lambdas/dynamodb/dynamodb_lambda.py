import os
import boto3


def handler(_, __):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["TABLE_NAME"])
    params = {
        "Key": {"pkey": "counter"},
        "ReturnValues": "UPDATED_NEW",
        "UpdateExpression": "SET counter = if_not_exists(counter, :start) + :inc",
        "ExpressionAttributeValues": {
            ":inc": 1,
            ":start": 0,
        },
    }
    response = table.update_item(**params)
    counter = response["Attributes"]["counter"]
    return {"statusCode": 200, "counter": counter}
