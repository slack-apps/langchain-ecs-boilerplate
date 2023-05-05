#!/usr/bin/env python3

import aws_cdk as cdk

from python_cdk_boilerplate.python_cdk_boilerplate_stack import PythonCdkBoilerplateStack

app = cdk.App()
PythonCdkBoilerplateStack(
    app, "PythonCdkBoilerplateStack",
    # env=cdk.Environment(region='us-east-2')
)

app.synth()
