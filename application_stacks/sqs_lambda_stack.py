import os

import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_sqs as sqs,
)
from constructs import Construct


class SqsLambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        queue_url = cdk.Fn.import_value("CdkSampleQueueUrl")
        queue_arn = cdk.Fn.import_value("CdkSampleQueueArn")
        queue = sqs.Queue.from_queue_arn(self, "SqsQueue", queue_arn=queue_arn)
        sqs_lambda = _lambda.Function(
            self,
            "SqsFunction",
            handler="sqs_lambda.handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset(os.path.join("lambdas", "sqs")),
            environment={"QUEUE_URL": queue_url},
        )
        queue.grant_send_messages(sqs_lambda)
