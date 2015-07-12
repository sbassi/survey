import csv
import os
import sys
import uuid
import settings
import boto.dynamodb2
from boto.dynamodb2.table import Table

AWS_ACCESS_KEY_ID = settings.AWS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET

try:
    csvfile = sys.argv[1]
except IndexError:
    print "Enter CSV filename as argument"
    exit(1)


# check if the file is present
"""
    c.execute('''CREATE TABLE users
             (email text, token text)''')
    c.execute('''CREATE TABLE result
             (token text, q1 text, q2 text, q3 text)''')
"""

conn = boto.dynamodb2.connect_to_region(
        'us-west-1',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

users = Table('survey2_users', connection=conn)

unique_emails = set()
with users.batch_write() as batch:
    with open(csvfile) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for line in csvreader:
            if line[0] not in unique_emails:
                batch.put_item(data={'email':line[0], 
                                 'token': str(uuid.uuid4()),
                                 })
                unique_emails.add(line[0])
            else:
                print "DUPE: %s"%line[0]

