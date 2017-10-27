import settings
import boto3
import sqlite3
import pickle
import csv, codecs
import xlsxwriter

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

conn = sqlite3.connect(SURVEY_DB_FILE)
c = conn.cursor()

all_data = {}
results_only = {}
for item in table.scan()['Items']:
    token = item['token']
    c.execute('SELECT email from users WHERE token=?', (token,))
    try:
        email = c.fetchone()[0]
        all_data[token] = {}
        all_data[token]['email'] = email
        all_data[token]['q1'] = item.get('q1')
        all_data[token]['q2'] = item.get('q2')
        all_data[token]['comment'] = item.get('comment')
    except TypeError:
        pass

workbook = xlsxwriter.Workbook('tandil.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write(0, 0,  'email')
worksheet.write(0, 1,  'q1')
worksheet.write(0, 2,  'q2')
worksheet.write(0, 3,  'comment')
for i, x in enumerate(all_data):
    worksheet.write(i+1, 0,  all_data[x].get('email'))
    worksheet.write(i+1, 1,  all_data[x].get('q1'))
    worksheet.write(i+1, 2,  all_data[x].get('q2'))
    worksheet.write(i+1, 3,  all_data[x].get('comment').encode('latin-1').decode('utf-8') if all_data[x].get('comment') else '')

workbook.close()
