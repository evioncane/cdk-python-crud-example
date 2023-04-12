#!/usr/bin/env python3

import aws_cdk as cdk

from kittens_storage_stack.kittens_storage_stack import KittensStorageStack


app = cdk.App()
KittensStorageStack(app, "KittensStorageStack")

app.synth()
