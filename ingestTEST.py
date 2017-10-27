
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

tokens = set()

try:
    csvfile = sys.argv[1]
except IndexError:
    print("Enter CSV filename as argument")
    exit(1)


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

# insert data
with open(csvfile) as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for line in csvreader:
        token = str(uuid.uuid4())
        c.execute("INSERT INTO users VALUES (?,?)",
                   (line[0], token))
        tokens.add(token)


pickle.dump(tokens, open(TOKENS_FILE,'wb'))
print('Token file created: {}'.format(TOKENS_FILE))

conn.commit()
conn.close()
