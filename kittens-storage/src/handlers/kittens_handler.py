import json
import os

import boto3

KITTENS_TABLE_NAME = os.environ['KITTENS_TABLE_NAME']
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(KITTENS_TABLE_NAME)


def add_kitten(event, context):
    print(event)

    kitten = event["body"]

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

    print(kitten_name)

    kitten = table.get_item(
        Key={
            "name": kitten_name,
        }
    )

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
