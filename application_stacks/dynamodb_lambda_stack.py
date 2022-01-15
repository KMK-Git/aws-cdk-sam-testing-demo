import os
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
)
from constructs import Construct


class DynamodbLambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        table_name = cdk.Fn.import_value("CdkSampleTableName")
        table = dynamodb.Table.from_table_name(self, "DynamodbTable", table_name)
        dynamodb_lambda = _lambda.Function(
            self,
            "DynamodbFunction",
            handler="dynamodb_lambda.handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset(os.path.join("lambdas", "dynamodb")),
            environment={"TABLE_NAME": table_name},
        )
        table.grant_write_data(dynamodb_lambda)
