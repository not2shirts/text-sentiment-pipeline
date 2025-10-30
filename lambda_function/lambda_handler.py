import json
import os
import urllib.request
import uuid
from datetime import datetime
import boto3
from decimal import Decimal


TABLE_NAME = os.environ.get("DYNAMODB_TABLE_NAME")


MICROSERVICE_URL = os.environ.get(
    "MICROSERVICE_URL"
)


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    try:

        body = json.loads(event.get("body", "{}"))
        comment = body.get("comment")

        if not comment:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No 'comment' field in body"}),
            }

        comment_id = str(uuid.uuid4())
        payload = {"text": comment}
        headers = {"Content-Type": "application/json"}

        req = urllib.request.Request(
            MICROSERVICE_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(req) as response:
            resp_body = response.read()
            sentiment_response = json.loads(resp_body)

    except Exception as e:
        print(f"Error calling sentiment microservice: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Could not analyze sentiment."}),
        }

    try:
        # score coming is a float DynamoDB cannot store Python floats (like 0.595).
        # one way to handle this is to convert floats to Decimal type. or store them as strings

        final_item = {
            "comment_id": comment_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",  # standard
            "original_comment": sentiment_response.get("text"),
            "sentiment": sentiment_response.get("sentiment"),
            "confidence": sentiment_response.get("confidence"),
            "score": str(sentiment_response.get("score")),
        }

        table.put_item(Item=final_item)

    except Exception as e:
        print(f"Error saving to DynamoDB: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Could not save comment to database."}),
        }

    # Return the item we just saved
    return {"statusCode": 200, "body": json.dumps(final_item)}
