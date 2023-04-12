import json

from dynamo_db import table


def handler(event, context):

    path_parameters = event.get("pathParameters")

    kitten_name = path_parameters.get("name")

    item = table.delete_item(Key={"name": kitten_name})

    if item.get("HTTPStatusCode") != 200:
        response_body = {
            "message": "Kitten Deleted!"
        }
    else:
        response_body = {
            "message": "Something went wrong!"
        }

    return {
        "statusCode": 200,
        "body": json.dumps(response_body)
    }
