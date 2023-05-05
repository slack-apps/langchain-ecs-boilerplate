#!/usr/bin/env python3

import aws_cdk as cdk

from langchain_ecs_boilerplate.langchain_ecs_boilerplate_stack import LangchainEcsBoilerplateStack

app = cdk.App()
LangchainEcsBoilerplateStack(
    app, "LangchainEcsBoilerplateStack",
    env=cdk.Environment(region='us-east-2')
)

app.synth()
