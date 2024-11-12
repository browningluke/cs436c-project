import boto3
import json
from botocore.exceptions import ClientError
from decimal import Decimal

dynamodb = boto3.resource("dynamodb", region_name="ca-central-1")

table = dynamodb.Table("cpsc436c-g9-statements")


def exampleInsert():
    item = {
        # Keys
        "UserId": "1",
        "YearMonth": "202409",
        # Values
        "transactions": [
            {
                "id": "123",
                "date": "2024-09-01",
                "vendor": "amazon",
                "category": "shopping",
                "amount": 120.5,
                "currency": "usd",
                "recurring": True,
                "type": "purchase",
                "location": "CA-BC",  # ISO 3166-2:CA
                "description": "Amazon Prime Subscription",
            }
        ],
    }

    try:
        # Insert item into the table
        item = json.loads(json.dumps(item), parse_float=Decimal)
        response = table.put_item(Item=item)
        print("Item successfully inserted:", response)

    except ClientError as e:
        print("Error inserting item:", e.response["Error"]["Message"])


def exampleQuery(uid, ym):
    try:
        # Query the table for the item with the primary key
        response = table.get_item(Key={"UserId": uid, "YearMonth": ym})

        # Check if item is found
        if "Item" in response:
            item = response["Item"]
            print("Item retrieved successfully:", item)
        else:
            print(f"Item not found.")

    except ClientError as e:
        print(f"Error querying item: {e.response['Error']['Message']}")


# exampleInsert()
exampleQuery("1", "202409")
