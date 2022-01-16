#!/usr/bin/env python3
import aws_cdk as cdk
from application_stacks.lambdas_stack import LambdasStack

app = cdk.App()


LambdasStack(app, "LambdasStack")

app.synth()
