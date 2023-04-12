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

        # Create a lambda layer
        db_layer = aws_lambda.LayerVersion(
            self,
            "DbLayer",
            code=aws_lambda.Code.from_asset("layer"),
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_9],
            description="DB Layer"
        )

        # Create Lambda functions
        kittens_add_function = aws_lambda.Function(
            self,
            id="KittenAddFunction",
            code=aws_lambda.Code.from_asset("src/api/post"),
            handler="add_kittens.handler",
            environment={
                "KITTENS_TABLE_NAME": kittens_table.table_name
            },
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            layers=[db_layer]
        )

        kittens_get_function = aws_lambda.Function(
            self,
            id="KittenGetFunction",
            code=aws_lambda.Code.from_asset("src/api/get"),
            handler="get_kittens.handler",
            environment={
                "KITTENS_TABLE_NAME": kittens_table.table_name
            },
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            layers=[db_layer]
        )

        kittens_list_function = aws_lambda.Function(
            self,
            id="KittenListFunction",
            code=aws_lambda.Code.from_asset("src/api/list"),
            handler="list_kittens.handler",
            environment={
                "KITTENS_TABLE_NAME": kittens_table.table_name
            },
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            layers=[db_layer]
        )

        kittens_delete_function = aws_lambda.Function(
            self,
            id="KittenDeleteFunction",
            code=aws_lambda.Code.from_asset("src/api/delete"),
            handler="delete_kittens.handler",
            environment={
                "KITTENS_TABLE_NAME": kittens_table.table_name
            },
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            layers=[db_layer]
        )

        # Grant Lambda permission to access DynamoDB
        kittens_table.grant_write_data(kittens_add_function)
        kittens_table.grant_read_data(kittens_get_function)
        kittens_table.grant_read_data(kittens_list_function)
        kittens_table.grant_write_data(kittens_delete_function)

        # Create a REST API Gateway
        api = aws_apigateway.RestApi(
            self, 'KittenAPI',
            rest_api_name='Kitten API',
            description='API for kitten storage'
        )

        # Create a Lambda integration

        post_integration = aws_apigateway.LambdaIntegration(kittens_add_function)
        get_integration = aws_apigateway.LambdaIntegration(kittens_get_function)
        list_integration = aws_apigateway.LambdaIntegration(kittens_list_function)
        delete_integration = aws_apigateway.LambdaIntegration(kittens_delete_function)

        # Add resource and method

        kittens_resource = api.root.add_resource("kittens")

        kittens_resource.add_method("POST", post_integration)
        kittens_resource.add_method("GET", list_integration)

        kitten_resource = kittens_resource.add_resource("{name}")

        kitten_resource.add_method("GET", get_integration)
        kitten_resource.add_method("DELETE", delete_integration)
