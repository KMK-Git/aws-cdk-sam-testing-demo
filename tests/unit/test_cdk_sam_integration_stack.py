import aws_cdk as core
import aws_cdk.assertions as assertions

from application_stacks.sqs_lambda_stack import SqsLambdaStack

# example tests. To run these tests, uncomment this file along with the example
# resource in application_stacks/sqs_lambda_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SqsLambdaStack(app, "cdk-sam-integration")
    template = assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
