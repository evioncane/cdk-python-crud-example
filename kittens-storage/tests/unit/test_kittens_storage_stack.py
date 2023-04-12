import aws_cdk as core
import aws_cdk.assertions as assertions

from kittens_storage_stack.kittens_storage_stack import KittensStorageStack

# example tests. To run these tests, uncomment this file along with the example
# resource in kittens_storage_stack/kittens_storage_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = KittensStorageStack(app, "kittens-storage")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
