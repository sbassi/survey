import settings
import boto.dynamodb2
from boto.dynamodb2.table import Table
from boto.dynamodb2.exceptions import ItemNotFound
import pickle
import pdb

AWS_ACCESS_KEY_ID = settings.AWS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET

conn = boto.dynamodb2.connect_to_region(
        'us-west-1',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

results = Table('survey2_results', connection=conn)

i = 0

all_data = {}

for item in results.scan():
    i+=1
    all_data[item['token']] = {}
    all_data[item['token']]['q1'] = item['q1']
    all_data[item['token']]['q2'] = item['q2']
    all_data[item['token']]['comment'] = item['comment']
    #pdb.set_trace()

pickle.dump(all_data, open('alldata','w'))

print i

#pdb.set_trace()