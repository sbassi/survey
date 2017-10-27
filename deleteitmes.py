#!/usr/bin/python3

"""Delete all items in the table"""

import settings
import boto3
import sqlite3

AWS_ACCESS_KEY_ID = settings.AWS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET
REGION = settings.REGION
TABLE_NAME = settings.TABLE_NAME
SURVEY_DB_FILE = settings.SURVEY_DB_FILE

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

results_only = {}
for i, item in enumerate(table.scan()['Items']):
    table.delete_item(Key={'token': item['token']})

print('Deleted {0} items'.format(i+1))
