import boto3
import json
import csv
from botocore.exceptions import ClientError
from decimal import Decimal
from collections import defaultdict

dynamodb = boto3.resource("dynamodb", region_name="ca-central-1")

table = dynamodb.Table("cpsc436c-g9-statements")

def check_table_connection(table_name):
    try:
        table = dynamodb.Table(table_name)
        response = table.table_status
        print(f"Connection successful! Table '{table_name}' status: {response}")
    except ClientError as e:
        print(f"Error connecting to table '{table_name}': {e.response['Error']['Message']}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

check_table_connection("cpsc436c-g9-statements")
print(table.attribute_definitions)

def process_csv(csv_path):
    try:
        grouped_items = defaultdict(list)
        
        with open(csv_path, mode = "r", encoding="utf-8-sig") as file:
            csv_reader = csv.DictReader(file)
            print(csv_reader.fieldnames)
            
            for row in csv_reader:
                transaction = {
                    "id": row["transactions.id"],
                    "date": row["transactions.date"],
                    "vendor": row["transactions.vendor"],
                    "category": row["transactions.category"],
                    "amount": Decimal(row["transactions.amount"]),
                    "currency": row["transactions.currency"],
                    "recurring": row["transactions.recurring"].lower() == "true",
                    "type": row["transactions.type"],
                    "location": row["transactions.location"],
                    "description": row["transactions.description"],
                }
                
                key = (row["UserId"], row["YearMonth"])
                grouped_items[key].append(transaction)
        
        dynamo_row = [
            {"UserId": user_id, "YearMonth": year_month, "transactions": transactions}
            for (user_id, year_month), transactions in grouped_items.items()
        ]
        print("Sucessfully read and formatted the csv")
        return dynamo_row
    except Exception as e:
        print("Error :", str(e))
        
def upload_to_dynamodb(items):
    try:
        print("Trying upload")
        for item in items:
            response = table.put_item(Item=item)
        print("Successfully inserted all rows")
        
    except ClientError as e:
        print(f"Error inserting item into DynamoDB: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        
transaction_rows = process_csv('user1data.csv')
upload_to_dynamodb(transaction_rows)

# def exampleInsert():
#     item = {
#         # Keys
#         "UserId": "1",
#         "YearMonth": "202409",
#         # Value
#         "transactions": [
#             {
#                 "id": "123",
#                 "date": "2024-09-01",
#                 "vendor": "amazon",
#                 "category": "shopping",
#                 "amount": 120.5,
#                 "currency": "usd",
#                 "recurring": True,
#                 "type": "purchase",
#                 "location": "CA-BC",  # ISO 3166-2:CA
#                 "description": "Amazon Prime Subscription",
#             }
#         ],
#     }

#     try:
#         # Insert item into the table
#         item = json.loads(json.dumps(item), parse_float=Decimal)
#         response = table.put_item(Item=item)
#         print("Item successfully inserted:", response)

#     except ClientError as e:
#         print("Error inserting item:", e.response["Error"]["Message"])


# def exampleQuery(uid, ym):
#     try:
#         # Query the table for the item with the primary key
#         response = table.get_item(Key={"UserId": uid, "YearMonth": ym})

#         # Check if item is found
#         if "Item" in response:
#             item = response["Item"]
#             print("Item retrieved successfully:", item)
#         else:
#             print(f"Item not found.")

#     except ClientError as e:
#         print(f"Error querying item: {e.response['Error']['Message']}")


# # exampleInsert()
# exampleQuery("1", "202409")
