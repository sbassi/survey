#!/usr/bin/python

"""Send email splitted
"""

import smtplib
import settings
import time
import pickle
from email.mime.text import MIMEText

SENDER_EMAIL = settings.SENDER_EMAIL

def send_email(email_list, subject, message=''):
    for recipient in email_list:
        # Msg body from template
        msg = MIMEText(message, 'plain', _charset='utf-8')
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient
        try:
            smtpObj = smtplib.SMTP(settings.SMTP_SERVER_NAME,
                                   settings.SMTP_SERVER_PORT)
            smtpObj.sendmail(SENDER_EMAIL, recipient, msg.as_string())
            print("Successfully sent email to {0}".format(recipient))
            time.sleep(.1)
        except smtplib.SMTPException:
            print("Error: unable to send email {0}".format(recipient))

no_repliers = ['sebastian.bassi@globant.com', 'sebastian.bassi@globant.com']
repliers = ['sebastian.bassi@globant.com', 'sebastian.bassi@globant.com']

repliers = pickle.load(open('repliers.pickle', "rb" ))
no_repliers = pickle.load(open('no_repliers.pickle', "rb" ))

# Email non repliers
subject = 'Sobre el email Survey from Globant'
body = """Ayer envié un e-mail con una encuesta. En dicho e-mail habia un error, la fecha
de respuesta estaba marcada como 15 de Octubre cuando debería haber sido 23 de Octubre.
Esto significa que me equivoqué en el e-mail y que aún hay tiempo para responder la encuesta.
Saludos,
Sebastián Bassi

PD: Para cualquier consulta sobre la encuesta escriban a survey@globant.com. La persona encargada de la misma es Ivan Wolcan (ivann.wolcan@globant.com)"""
send_email(no_repliers, subject, body)

print('Responders:')
subject = 'Gracias por responder la encuesta'
body = """Ayer envié un e-mail con una encuesta. En dicho e-mail habia un error, la fecha de respuesta estaba marcada como 15 de Octubre cuando debería haber sido 23 de Octubre.
Esto significa que me equivoqué, pero el sistema registró tu respuesta asi que no hay que hacer nada mas hasta la próxima encuesta.

Saludos,
Sebastián Bassi

PD: Para cualquier consulta sobre la encuesta escriban a survey@globant.com. La persona encargada de la misma es Ivan Wolcan (ivann.wolcan@globant.com)"""
send_email(repliers, subject, body)
