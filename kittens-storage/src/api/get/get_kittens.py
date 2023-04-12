import json

from dynamo_db import table


def handler(event, context):

    path_parameters = event.get("pathParameters")

    kitten_name = path_parameters.get("name")

    db_response = table.get_item(
        Key={
            "name": kitten_name,
        }
    )

    kitten = db_response.get("Item")

    if kitten:

        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(kitten)
        }
    else:
        response = {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": '{"message": "Kitten not found!"}'
        }

    return response
