import json
import os

import boto3

KITTENS_TABLE_NAME = os.environ.get("KITTENS_TABLE_NAME")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(KITTENS_TABLE_NAME)


def add_kitten(event, context):
    print(KITTENS_TABLE_NAME)
    print(event)

    kitten = json.loads(event["body"])
    print(kitten)

    item = table.put_item(
        Item=kitten
    )

    print(item)

    response_body = {"message": "Kitten added"}

    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(response_body)
    }

    return response


def get_kitten(event, context):
    print(event)

    path_parameters = event.get("pathParameters")

    kitten_name = path_parameters.get("name")

    db_response = table.get_item(
        Key={
            "name": kitten_name,
        }
    )

    kitten = db_response["Item"]

    print(f"After DB: {kitten}")

    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(kitten)
    }

    return response


def list_kittens(event, context):
    db_response = table.scan()
    kittens = db_response["Items"]
    return {
        "statusCode": 200,
        "body": json.dumps(kittens)
    }


def delete_kitten(event, context):
    print(event)

    path_parameters = event.get("pathParameters")

    kitten_name = path_parameters.get("name")

    item = table.delete_item(Key={"name": kitten_name})

    print(item)

    return {
        "statusCode": 200,
        "body": json.dumps("Kitten Deleted!")
    }
