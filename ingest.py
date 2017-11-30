# create/update SQLite out of CSV
import csv
import sqlite3
import os
import sys
import uuid
import settings
import pickle

SURVEY_DB_FILE = settings.SURVEY_DB_FILE
TOKENS_FILE = settings.TOKENS_FILE
REGEX = settings.LOCAL_REGEX
LOCATED_CSV = settings.TARGET_CSV
INPUTCSV = settings.INPUTCSV

if not os.path.isfile(INPUTCSV):
    exit()


with open(INPUTCSV) as csvfh:
    with open(LOCATED_CSV, 'w') as outfh:
        csvreader = csv.reader(csvfh, delimiter=',', quotechar='"')
        for line in csvreader:
            if line[15].startswith(REGEX):
                outfh.write(line[0]+'\n')

print("Wrote {}".format(LOCATED_CSV))



tokens = set()

# check if the file is present
if os.path.isfile(SURVEY_DB_FILE):
    conn = sqlite3.connect(SURVEY_DB_FILE)
    # add data from csv file into DB
    print("File already present")
    c = conn.cursor()
else:
    # create file and DB from 0
    conn = sqlite3.connect(SURVEY_DB_FILE)
    print('New file created: {}'.format(SURVEY_DB_FILE))
    c = conn.cursor()
    c.execute('''CREATE TABLE users
             (email text, token text)''')

# insert data in pickle and DB
with open(LOCATED_CSV) as csvfh:
    csvreader = csv.reader(csvfh, delimiter=',', quotechar='"')
    for line in csvreader:
        token = str(uuid.uuid4())
        c.execute("INSERT INTO users VALUES (?,?)",
                   (line[0], token))
        tokens.add(token)

pickle.dump(tokens, open(TOKENS_FILE,'wb'))
print('Token file created: {0}'.format(TOKENS_FILE))

conn.commit()
conn.close()
