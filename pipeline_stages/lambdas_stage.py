import aws_cdk as cdk
from constructs import Construct

from application_stacks.lambdas_stack import LambdasStack


class LambdasStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        LambdasStack(self, "LambdasStack")
