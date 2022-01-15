from aws_cdk import (
    Stack,
    Stage,
    pipelines as pipelines,
    aws_ssm as ssm,
)
from constructs import Construct


class PipelineStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        supporting_resources_stage: Stage,
        lambdas_stage: Stage,
        **kwargs
    ):
        super().__init__(scope, construct_id, **kwargs)

        cdk_codepipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.connection(
                    "KMK-Git/aws-cdk-sam-testing-demo",
                    "main",
                    connection_arn=ssm.StringParameter.value_for_string_parameter(
                        self,
                        "codestar_connection_arn",
                    ),
                ),
                commands=[
                    "pip install -r requirements.txt",
                    "npm install -g aws-cdk",
                    "cdk synth",
                ],
            ),
        )
        cdk_codepipeline.add_stage(
            supporting_resources_stage,
            pre=[
                pipelines.ConfirmPermissionsBroadening(
                    "CheckSupporting", stage=supporting_resources_stage
                )
            ],
        )
        cdk_codepipeline.add_stage(
            lambdas_stage,
            pre=[
                pipelines.ConfirmPermissionsBroadening(
                    "CheckLambda", stage=lambdas_stage
                )
            ],
        )
