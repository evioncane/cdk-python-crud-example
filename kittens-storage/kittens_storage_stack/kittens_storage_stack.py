from aws_cdk import (
    Stack,
    aws_dynamodb,
    aws_lambda,
    aws_apigateway
)

from constructs import Construct


class KittensStorageStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create DynamoDB table
        partition_key = aws_dynamodb.Attribute(name="name", type=aws_dynamodb.AttributeType.STRING)
        kittens_table = aws_dynamodb.Table(self, "kitten_table", partition_key=partition_key)

        # Create Lambda function
        # kittens_add_function = aws_lambda.Function(
        #     self,
        #     id="KittenAddFunction",
        #     code=aws_lambda.Code.from_asset("src"),
        #     handler="handlers.kittens_handler.add_kitten",
        #     runtime=aws_lambda.Runtime.PYTHON_3_9,
        #     environment={
        #         'CONTENT_TYPE': 'application/json',
        #         'ACCEPT': 'application/json'
        #     }
        # )
        # kittens_add_function.add_environment("KITTENS_TABLE_NAME", kittens_table.table_name)

        kittens_get_function = aws_lambda.Function(
            self,
            id="KittenGetFunction",
            code=aws_lambda.Code.from_asset("src"),
            handler="handlers.kittens_handler.get_kitten",
            runtime=aws_lambda.Runtime.PYTHON_3_9
        )
        kittens_get_function.add_environment("KITTENS_TABLE_NAME", kittens_table.table_name)

        # kittens_list_function = aws_lambda.Function(
        #     self,
        #     id="KittenListFunction",
        #     code=aws_lambda.Code.from_asset("src"),
        #     handler="handlers.kittens_handler.list_kittens",
        #     runtime=aws_lambda.Runtime.PYTHON_3_9
        # )
        # kittens_list_function.add_environment("KITTENS_TABLE_NAME", kittens_table.table_name)
        #
        # kittens_delete_function = aws_lambda.Function(
        #     self,
        #     id="KittenDeleteFunction",
        #     code=aws_lambda.Code.from_asset("src"),
        #     handler="handlers.kittens_handler.delete_kitten",
        #     runtime=aws_lambda.Runtime.PYTHON_3_9
        # )
        # kittens_delete_function.add_environment("KITTENS_TABLE_NAME", kittens_table.table_name)

        # Grant Lambda permission to access DynamoDB
        # kittens_table.grant_write_data(kittens_add_function)
        kittens_table.grant_read_data(kittens_get_function)
        # kittens_table.grant_read_data(kittens_list_function)
        # kittens_table.grant_write_data(kittens_delete_function)

        # Create a REST API Gateway
        # api = aws_apigateway.RestApi(self, 'MyRestApi',
        #                              rest_api_name='My API Gateway'
        #                              )
        # Create the API Gateway
        api = aws_apigateway.LambdaRestApi(
            self, 'MyAPI',
            handler=kittens_get_function,
            proxy=False
        )

        # Create a Lambda integration
        # post_integration = aws_apigateway.LambdaIntegration(kittens_add_function,
        #                                                     proxy=False,
        #                                                     request_templates={
        #                                                         "application/json": '{"body": $input.json("$")}'},
        #                                                     integration_responses=[{
        #                                                         "statusCode": "200",
        #                                                         "responseTemplates": {
        #                                                             "application/json": "$input.path('$.body')"
        #                                                         }
        #                                                     }]
        #                                                     )
        #
        # get_all_integration = aws_apigateway.LambdaIntegration(kittens_list_function,
        #                                                        proxy=False,
        #                                                        request_templates={
        #                                                            "application/json": '{"body": $input.json("$")}'},
        #                                                        integration_responses=[{
        #                                                            "statusCode": "200",
        #                                                            "responseTemplates": {
        #                                                                "application/json": "$input.path('$.body')"
        #                                                            }
        #                                                        }]
        #                                                        )

        get_integration = aws_apigateway.LambdaIntegration(kittens_get_function, proxy=False)

        # delete_integration = aws_apigateway.LambdaIntegration(kittens_delete_function,
        #                                                       proxy=False,
        #                                                       request_templates={
        #                                                           "application/json": '{"body": $input.json("$")}'},
        #                                                       integration_responses=[{
        #                                                           "statusCode": "200",
        #                                                           "responseTemplates": {
        #                                                               "application/json": "$input.path('$.body')"
        #                                                           }
        #                                                       }]
        #                                                       )

        # Add a resource and method to the API Gateway
        kittens_resource = api.root.add_resource('kittens')

        kitten_resource = kittens_resource.add_resource("{name}")

        # kittens_resource.add_method('POST', post_integration,
        #                             request_parameters={
        #                                 'method.request.header.Accept': True,
        #                                 'method.request.header.Content-Type': True
        #                             },
        #                             request_models={
        #                                 'application/json': aws_apigateway.Model.EMPTY_MODEL,
        #                             },
        #                             method_responses=[{
        #                                 'statusCode': '200',
        #                                 'responseModels': {
        #                                     'application/json': aws_apigateway.Model.EMPTY_MODEL,
        #                                 },
        #                                 'responseParameters': {
        #                                     'method.response.header.Access-Control-Allow-Origin': True,
        #                                     'method.response.header.Content-Type': True
        #                                 }
        #                             }]
        #                             )
        # kittens_resource.add_method('GET', get_all_integration,
        #                             request_parameters={
        #                                 'method.request.header.Accept': True,
        #                                 'method.request.header.Content-Type': True
        #                             },
        #                             request_models={
        #                                 'application/json': aws_apigateway.Model.EMPTY_MODEL,
        #                             },
        #                             method_responses=[{
        #                                 'statusCode': '200',
        #                                 'responseModels': {
        #                                     'application/json': aws_apigateway.Model.EMPTY_MODEL,
        #                                 },
        #                                 'responseParameters': {
        #                                     'method.response.header.Access-Control-Allow-Origin': True,
        #                                     'method.response.header.Content-Type': True
        #                                 }
        #                             }]
        #                             )

        kitten_resource.add_method('GET', get_integration,
                                   request_parameters={
                                       "method.request.querystring.age": True
                                   }
                                   )


        # kitten_resource.add_method('DELETE', delete_integration,
        #                            request_parameters={
        #                                'method.request.header.Accept': True,
        #                                'method.request.header.Content-Type': True
        #                            },
        #                            request_models={
        #                                'application/json': aws_apigateway.Model.EMPTY_MODEL,
        #                            },
        #                            method_responses=[{
        #                                'statusCode': '200',
        #                                'responseModels': {
        #                                    'application/json': aws_apigateway.Model.EMPTY_MODEL,
        #                                },
        #                                'responseParameters': {
        #                                    'method.response.header.Access-Control-Allow-Origin': True,
        #                                    'method.response.header.Content-Type': True
        #                                }
        #                            }]
        #                            )
