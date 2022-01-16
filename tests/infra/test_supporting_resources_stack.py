import aws_cdk as core
import aws_cdk.assertions as assertions

from application_stacks.supporting_resources_stack import SupportingResourcesStack


def test_supporting_resources_created():
    app = core.App()
    stack = SupportingResourcesStack(app, "SupportingResourcesStack")
    template = assertions.Template.from_stack(stack)
    template.has_resource("AWS::SQS::Queue", {})
    template.resource_count_is("AWS::SQS::Queue", 1)
    template.has_resource_properties(
        "AWS::DynamoDB::Table",
        {
            "KeySchema": [{"AttributeName": "pkey", "KeyType": "HASH"}],
            "AttributeDefinitions": [{"AttributeName": "pkey", "AttributeType": "S"}],
            "BillingMode": "PAY_PER_REQUEST",
        },
    )
    template.resource_count_is("AWS::DynamoDB::Table", 1)
