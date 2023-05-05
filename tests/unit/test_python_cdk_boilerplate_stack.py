import aws_cdk as core
import aws_cdk.assertions as assertions

from langchain_ecs_boilerplate.langchain_ecs_boilerplate_stack import LangchainEcsBoilerplateStack


# example tests. To run these tests, uncomment this file along with the example
# resource in langchain_ecs_boilerplate/langchain_ecs_boilerplate_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = LangchainEcsBoilerplateStack(app, "langchain-ecs-boilerplate")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
