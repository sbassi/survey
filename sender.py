#!/usr/bin/python

import smtplib
from jinja2 import Template
import settings
import sqlite3
import time
import codecs
from email.mime.text import MIMEText

# Load external data
SENDER_EMAIL = settings.SENDER_EMAIL
SENDER_NAME = settings.SENDER_NAME
SURVEY_DB_FILE = settings.SURVEY_DB_FILE
SUBJECT = settings.SUBJECT
SUBMIT_POST_SERVER = settings.SUBMIT_POST_SERVER
IMGSERVER = settings.IMGSERVER

# get list of receivers
conn = sqlite3.connect(SURVEY_DB_FILE)
c = conn.cursor()

c.execute("SELECT * FROM users")
data = c.fetchall()

for record in data:
    recipient = record[0]
    token = record[1]
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
        print("Successfully sent email to {0}".format(recipient))
        time.sleep(.4)
    except smtplib.SMTPException:
        print("Error: unable to send email {0}".format(recipient))
