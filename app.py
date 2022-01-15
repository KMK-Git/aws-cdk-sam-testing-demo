#!/usr/bin/env python3
import aws_cdk as cdk
from pipeline_stack.pipeline import PipelineStack
from pipeline_stages.lambdas_stage import LambdasStage
from pipeline_stages.supporting_resources_stage import SupportingResourcesStage

app = cdk.App()


PipelineStack(
    app,
    "PipelineStack",
    supporting_resources_stage=SupportingResourcesStage(
        app, "SupportingResourcesStage"
    ),
    lambdas_stage=LambdasStage(app, "LambdaStage"),
)

app.synth()
