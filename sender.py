#!/usr/bin/python

import smtplib
from jinja2 import Template
import settings
import sqlite3
import time

# Load external data
SENDER_EMAIL = settings.SENDER_EMAIL
SENDER_NAME = settings.SENDER_NAME
SURVEY_DB_FILE = settings.SURVEY_DB_FILE
SUBJECT = settings.SUBJECT
SUBMIT_POST_SERVER = settings.SUBMIT_POST_SERVER
IMGSERVER = setting.imgserver

# get list of receivers
conn = sqlite3.connect(SURVEY_DB_FILE)
c = conn.cursor()

c.execute("SELECT * FROM users")
data = c.fetchall()

for record in data:
    recipient = record[0]
    token = record[1]
    receivers = [recipient]
    message_header = """From: {sender_name} <{sender_email}>
To: <{recipient}>
MIME-Version: 1.0
Content-type: text/html
Subject: {subject}


""".format(sender_name = SENDER_NAME,
    sender_email = SENDER_EMAIL,
    recipient = recipient,
    subject = SUBJECT,
    imgserver = IMGSERVER)
    # Msg body from template
    t = Template(open('templates/email.html').read())
    message_body = t.render(mailto=recipient, 
                    submit_url=SUBMIT_POST_SERVER,
                    token=token)
    
    message = message_header + message_body
    try:
        smtpObj = smtplib.SMTP(settings.SMTP_SERVER_NAME, 
        	                   settings.SMTP_SERVER_PORT)
        smtpObj.sendmail(SENDER_EMAIL, receivers, message)         
        print "Successfully sent email"
        time.sleep(1)
    except smtplib.SMTPException:
        print "Error: unable to send email"