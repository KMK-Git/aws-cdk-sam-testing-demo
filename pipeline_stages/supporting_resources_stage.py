import aws_cdk as cdk
from constructs import Construct
from application_stacks.supporting_resources_stack import SupportingResourcesStack


class SupportingResourcesStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self.stack = SupportingResourcesStack(self, "SupportingResourcesStack")
