#!/usr/bin/python

import smtplib
from jinja2 import Template
import settings
import time
import codecs
from email.mime.text import MIMEText
import boto.dynamodb2
from boto.dynamodb2.table import Table


# Load external data
SENDER_EMAIL = settings.SENDER_EMAIL
SENDER_NAME = settings.SENDER_NAME
SUBJECT = settings.SUBJECT
SUBMIT_POST_SERVER = settings.SUBMIT_POST_SERVER
IMGSERVER = settings.IMGSERVER
AWS_ACCESS_KEY_ID = settings.AWS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET

# get list of receivers
conn = boto.dynamodb2.connect_to_region(
        'us-west-1',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

users = Table('survey2_users', connection=conn)
data = users.scan()

for record in data:
    recipient = record['email']
    token = record['token']
    #print recipient, token
    receivers = [recipient]
    # Msg body from template
    t = Template(codecs.open('templates/email.html', 'r', 'utf-8').read())
    message_body = t.render(mailto=recipient, 
                    submit_url=SUBMIT_POST_SERVER,
                    token=token, imgserver = IMGSERVER)
    
    message = message_body
    msg = MIMEText(message, 'html', _charset='utf-8')
    msg['Subject'] = SUBJECT
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient
    try:

        smtpObj = smtplib.SMTP(settings.SMTP_SERVER_NAME, 
        	                   settings.SMTP_SERVER_PORT)
        smtpObj.sendmail(SENDER_EMAIL, receivers, msg.as_string())         
        print "Successfully sent email"
        time.sleep(1)
    except smtplib.SMTPException:
        print "Error: unable to send email"