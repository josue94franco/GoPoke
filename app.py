#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_go_poket.cdk_go_poket_stack import CdkGoPoketStack


app = cdk.App()
CdkGoPoketStack(app, "CdkGoPoketStack"
   
    )

app.synth()
