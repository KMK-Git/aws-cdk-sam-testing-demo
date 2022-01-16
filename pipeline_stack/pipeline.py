from aws_cdk import (
    Stack,
    pipelines as pipelines,
    aws_ssm as ssm,
    aws_codebuild as codebuild,
)
from constructs import Construct

from pipeline_stages.lambdas_stage import LambdasStage
from pipeline_stages.supporting_resources_stage import SupportingResourcesStage


class PipelineStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        supporting_resources_stage: SupportingResourcesStage,
        lambdas_stage: LambdasStage,
        **kwargs
    ):
        super().__init__(scope, construct_id, **kwargs)
        source = pipelines.CodePipelineSource.connection(
            "KMK-Git/aws-cdk-sam-testing-demo",
            "main",
            connection_arn=ssm.StringParameter.value_for_string_parameter(
                self,
                "codestar_connection_arn",
            ),
        )
        cdk_codepipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=source,
                install_commands=[
                    "pip install -r requirements.txt",
                    "npm install -g aws-cdk",
                ],
                commands=[
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
                pipelines.CodeBuildStep(
                    "SAMTesting",
                    input=source,
                    env_from_cfn_outputs={
                        "QUEUE_URL": supporting_resources_stage.stack.queue_url,
                        "TABLE_NAME": supporting_resources_stage.stack.table_name,
                    },
                    install_commands=[
                        "pip install -r requirements.txt",
                        "npm install -g aws-cdk",
                        "curl --version",
                        "mkdir testoutput",
                    ],
                    commands=[
                        'cdk synth -a "python synth_lambdas_stack.py" -o sam.out',
                        'echo "{\\""SqsLambdaFunction\\"": {\\""QUEUE_URL\\"": \\""$QUEUE_URL\\""},'
                        + '\\""DynamodbLambdaFunction\\"": {\\""TABLE_NAME\\"": \\""$TABLE_NAME\\"" }}"'
                        + " > locals.json",
                        'sam local invoke -t "sam.out/LambdasStack.template.json" --env-vars locals.json'
                        + ' --no-event "DynamodbLambdaFunction"',
                        'sam local invoke -t "sam.out/LambdasStack.template.json" --env-vars locals.json'
                        + ' --no-event "SqsLambdaFunction"',
                        "nohup sam local start-api -t sam.out/LambdasStack.template.json"
                        + " --env-vars locals.json > testoutput/testing.log & ",
                        "",
                        "sleep 30",
                        "curl --fail http://127.0.0.1:3000/sqs",
                        "curl --fail http://127.0.0.1:3000/dynamodb",
                    ],
                    build_environment=codebuild.BuildEnvironment(
                        build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
                        privileged=True,
                        compute_type=codebuild.ComputeType.SMALL,
                    ),
                    primary_output_directory="testoutput/",
                ),
                pipelines.ConfirmPermissionsBroadening(
                    "CheckLambda", stage=lambdas_stage
                ),
            ],
        )
