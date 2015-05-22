#!/usr/bin/python

import smtplib
from jinja2 import Template
import settings
import sqlite3

# Load external data


SENDER_EMAIL = settings.SENDER_EMAIL
SENDER_NAME = settings.SENDER_NAME



# get list of receivers




receivers = ['virginia.gonzalez@globant.com']

message_header = """From: XXX <survey@globant.com>
To: To Person <virginia.gonzalez@globant.com>
MIME-Version: 1.0
Content-type: text/html
Subject: Prueba de mail en HTML


"""

try:
    smtpObj = smtplib.SMTP(settings.SMTP_SERVER_NAME, 
    	                   settings.SMTP_SERVER_PORT)
    smtpObj.sendmail(SENDER_EMAIL, receivers, message)         
    print "Successfully sent email"
except SMTPException:
    print "Error: unable to send email"