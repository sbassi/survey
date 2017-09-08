from bottle import (post, run, template, request,
	                get, static_file, template)
import settings
import codecs
import pickle

import boto.dynamodb2
from boto.dynamodb2.table import Table
from boto.dynamodb2.exceptions import ItemNotFound

#from jinja2 import Template

BASEDIR = settings.BASEDIR
AWS_ACCESS_KEY_ID = settings.AWS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET
TOKENS_FILE = settings.TOKENS_FILE
TABLE_NAME = settings.TABLE_NAME

@get('/')
def home():
    return template(codecs.open(BASEDIR + 'templates/base.html', 'r', 'utf-8').read(),
                    msg='Server for internal survey', state='default')


@post('/surveypost/<token>')
def index(token):

    conn = boto.dynamodb2.connect_to_region(
        'us-east-1',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    def _authenticate(token):
       tokens = pickle.load(open(TOKENS_FILE, "rb" ) )
       if token in tokens:
           return True
       else:
           return False

    def _submited(token):
        results = Table(TABLE_NAME, connection=conn)
        try:
            return results.get_item(token=token)
        except ItemNotFound:
            return False

    if _authenticate(token) and not _submited(token):
        #print token
        q1 = request.forms.get('delivery')
        q2 = request.forms.get('feeling')
        comment = request.forms.get('comment')
        # CHANGE FOR AWS
        results = Table(TABLE_NAME, connection=conn)
        results.put_item(data={
                        'token': token,
                        'q1': q1,
                        'q2': q2,
                        'comment': comment,
                        })
        conn.close()
    elif _submited(token):
        conn.close()

        return template(codecs.open(BASEDIR + 'templates/base.html', 'r', 'utf-8').read(),
                    msg='Survey already submitted', state='danger')

    else:
        return template(codecs.open(BASEDIR + 'templates/base.html', 'r', 'utf-8').read(),
                    msg='Unkown user', state='danger')



    return template(codecs.open(BASEDIR + 'templates/base.html', 'r', 'utf-8').read(),
                    msg='Thank you!', state='success')



if __name__ == '__main__':
    run(host='localhost', port=8080)
