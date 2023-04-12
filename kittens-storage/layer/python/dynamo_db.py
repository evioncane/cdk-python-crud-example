import os
import boto3

KITTENS_TABLE_NAME = os.environ.get("KITTENS_TABLE_NAME")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(KITTENS_TABLE_NAME)
