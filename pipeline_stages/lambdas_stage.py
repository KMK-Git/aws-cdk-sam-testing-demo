import aws_cdk as cdk
from constructs import Construct
from application_stacks.dynamodb_lambda_stack import DynamodbLambdaStack
from application_stacks.sqs_lambda_stack import SqsLambdaStack


class LambdasStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        SqsLambdaStack(self, "SqsLambdaStack")
        DynamodbLambdaStack(self, "DynamodbLambdaStack")
