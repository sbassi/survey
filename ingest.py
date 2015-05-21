
# create/update SQLite out of CSV

import csv
import sqlite3
import os
import sys
import uuid

SURVEY_DB_FILE = 'survey.db'

try:
    csvfile = sys.argv[1]
except IndexError:
    print "Enter CSV filename as argument"
    exit(1)


# check if the file is present
if os.path.isfile(SURVEY_DB_FILE):
    conn = sqlite3.connect(SURVEY_DB_FILE)
    # add data from csv file into DB
    print "y"
    c = conn.cursor()
else:
    # create file and DB from 0
    conn = sqlite3.connect(SURVEY_DB_FILE)
    print 'n'
    c = conn.cursor()
    c.execute('''CREATE TABLE users
             (email text, token text)''')
    c.execute('''CREATE TABLE result
             (token text, q1 text, q2 text, q3 text)''')


# insert data
with open(csvfile) as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for line in csvreader:
        c.execute("INSERT INTO users VALUES (?,?)", (line[0],str(uuid.uuid4())))

conn.commit()
conn.close()
