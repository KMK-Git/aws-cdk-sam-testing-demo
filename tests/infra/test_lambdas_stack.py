import aws_cdk as core
import aws_cdk.assertions as assertions

from application_stacks.lambdas_stack import LambdasStack


def test_lambdas_created():
    app = core.App()
    stack = LambdasStack(app, "LambdasStack")
    template = assertions.Template.from_stack(stack)
    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Environment": {
                "Variables": {"QUEUE_URL": {"Fn::ImportValue": "CdkSampleQueueUrl"}}
            },
            "Handler": "sqs_lambda.handler",
            "Runtime": "python3.9",
        },
    )
    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Environment": {
                "Variables": {"TABLE_NAME": {"Fn::ImportValue": "CdkSampleTableName"}}
            },
            "Handler": "dynamodb_lambda.handler",
            "Runtime": "python3.9",
        },
    )
    template.resource_count_is("AWS::Lambda::Function", 2)
