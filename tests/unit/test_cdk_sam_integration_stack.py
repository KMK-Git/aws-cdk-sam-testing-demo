import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_sam_integration.cdk_sam_integration_stack import CdkSamIntegrationStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_sam_integration/cdk_sam_integration_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkSamIntegrationStack(app, "cdk-sam-integration")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
