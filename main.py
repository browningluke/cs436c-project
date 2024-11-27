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
        
transaction_rows = process_csv('user3data.csv')
upload_to_dynamodb(transaction_rows)