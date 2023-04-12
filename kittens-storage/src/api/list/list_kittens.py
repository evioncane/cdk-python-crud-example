import json

from dynamo_db import table


def handler(event, context):
    db_response = table.scan()
    kittens = db_response.get("Items")
    return {
        "statusCode": 200,
        "body": json.dumps(kittens)
    }
