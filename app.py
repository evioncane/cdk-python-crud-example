#!/usr/bin/env python3

import aws_cdk as cdk

from pyranha.pyranha_stack import PyranhaStack


app = cdk.App()
PyranhaStack(app, "pyranha")

app.synth()
