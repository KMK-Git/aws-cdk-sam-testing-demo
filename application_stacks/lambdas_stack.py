import os

import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_sqs as sqs,
    aws_dynamodb as dynamodb,
    aws_lambda_event_sources as events,
)
from constructs import Construct


class LambdasStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Create function to send a message to a SQS queue
        queue_url = cdk.Fn.import_value(
            "CdkSampleQueueUrl"
        )  # Import values from supporting resources stack
        queue_arn = cdk.Fn.import_value("CdkSampleQueueArn")
        queue = sqs.Queue.from_queue_arn(self, "SqsQueue", queue_arn=queue_arn)
        sqs_lambda = _lambda.Function(
            self,
            "SqsFunction",
            handler="sqs_lambda.handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset(os.path.join("lambdas", "sqs")),
            environment={"QUEUE_URL": queue_url},
            events=[events.ApiEventSource("GET", "/sqs")],
        )
        sqs_lambda_base: _lambda.CfnFunction = sqs_lambda.node.default_child
        sqs_lambda_base.override_logical_id("SqsLambdaFunction")
        queue.grant_send_messages(sqs_lambda)
        # Create function to increment counter in a DynamoDB table
        table_name = cdk.Fn.import_value(
            "CdkSampleTableName"
        )  # Import values from supporting resources stack
        table = dynamodb.Table.from_table_name(self, "DynamodbTable", table_name)
        dynamodb_lambda = _lambda.Function(
            self,
            "DynamodbFunction",
            handler="dynamodb_lambda.handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset(os.path.join("lambdas", "dynamodb")),
            environment={"TABLE_NAME": table_name},
            events=[events.ApiEventSource("GET", "/dynamodb")],
        )
        dynamodb_lambda_base: _lambda.CfnFunction = dynamodb_lambda.node.default_child
        dynamodb_lambda_base.override_logical_id("DynamodbLambdaFunction")
        table.grant_write_data(dynamodb_lambda)
