import settings
import boto.dynamodb2
from boto.dynamodb2.table import Table
from boto.dynamodb2.exceptions import ItemNotFound
import pickle
import pdb
import csv, codecs, cStringIO

AWS_ACCESS_KEY_ID = settings.AWS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        print row
        pdb.set_trace()
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

conn = boto.dynamodb2.connect_to_region(
        'us-west-1',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

results = Table('survey2_results', connection=conn)
users = Table('survey2_users', connection=conn)

i = 0

all_data = {}

for item in results.scan():
    i+=1
    all_data[item['token']] = {}
    all_data[item['token']]['q1'] = item['q1']
    all_data[item['token']]['q2'] = item['q2']
    all_data[item['token']]['comment'] = item['comment']
    #pdb.set_trace()

usersd = {}

for item in users.scan():
    usersd[item['token']] = item['email']
    
for item in all_data:
    all_data[item]['email'] = usersd[item]

pickle.dump(all_data, open('results','w'))

#with open('resultados.csv')
with open('resultados.csv', 'wb') as csvfile:
    csvw = UnicodeWriter(csvfile, delimiter='\t',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for x in all_data:
		csvw.writerow([x, all_data[x]['email'], all_data[x]['q1'],
		all_data[x]['q2'], all_data[x]['comment']])


