from aws_cdk import (
    Stack,
    CfnOutput,
    aws_sqs as sqs,
    aws_dynamodb as dynamodb,
)
from constructs import Construct


class SupportingResourcesStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        queue = sqs.Queue(self, "SqsQueue")
        table = dynamodb.Table(
            self,
            "DynamodbTable",
            partition_key=dynamodb.Attribute(
                name="pkey", type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        )
        CfnOutput(
            self, "QueueUrl", value=queue.queue_url, export_name="CdkSampleQueueUrl"
        )
        CfnOutput(
            self, "QueueArn", value=queue.queue_arn, export_name="CdkSampleQueueArn"
        )
        CfnOutput(
            self, "TableName", value=table.table_name, export_name="CdkSampleTableName"
        )
