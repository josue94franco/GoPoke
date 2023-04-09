import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_go_poket.cdk_go_poket_stack import CdkGoPoketStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_go_poket/cdk_go_poket_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkGoPoketStack(app, "cdk-go-poket")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
