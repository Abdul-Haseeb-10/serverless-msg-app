#!/usr/bin/env python3
import os
import aws_cdk as cdk
from serverless_msg_app.serverless_msg_app_stack import CalabrioApp

app = cdk.App()
CalabrioApp(app, "CalabrioApp")
app.synth()