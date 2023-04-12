import json

from dynamo_db import table


def handler(event, context):
    kitten = json.loads(event["body"])

    item = table.put_item(
        Item=kitten
    )

    response_body = {
        "message": "Kitten added"
    }

    if item.get("HTTPStatusCode") != 200:
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(response_body)
        }

    response_body["kitten"] = json.dumps(kitten)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response_body)
    }
