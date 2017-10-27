import settings
import boto3
import sqlite3
import time
import pickle

AWS_ACCESS_KEY_ID = settings.AWS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET
REGION = settings.REGION
TABLE_NAME = settings.TABLE_NAME
SURVEY_DB_FILE = settings.SURVEY_DB_FILE
SENDER_EMAIL = settings.SENDER_EMAIL


all_people = set()

with open('cordoba.csv') as fh:
    for line in fh:
        all_people.add(line.replace('\n',''))

print(len(all_people))
time.sleep(4)
# repliers
repliers = set()
dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

conn = sqlite3.connect(SURVEY_DB_FILE)
c = conn.cursor()

all_data = {}
results_only = {}
for item in table.scan()['Items']:
    token = item['token']
    c.execute('SELECT email from users WHERE token=?', (token,))
    email = c.fetchone()[0]
    repliers.add(email)

print(len(repliers))
no_repliers = all_people - repliers
print(len(no_repliers))

pickle.dump(repliers, open('repliers.pickle','wb'))
pickle.dump(no_repliers, open('no_repliers.pickle','wb'))
