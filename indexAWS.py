from bottle import (post, run, template, request, 
	                get, static_file, template)
#import sqlite3
import settings
import codecs

#from jinja2 import Template

#SURVEY_DB_FILE = settings.SURVEY_DB_FILE
BASEDIR = settings.BASEDIR
AWS_ACCESS_KEY_ID = settings.AWS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET


@get('/')
def home():
    return template(codecs.open(BASEDIR + 'templates/base.html', 'r', 'utf-8').read(),        
    	            msg='Server for internal survey', state='default')


@post('/surveypost/<token>')
def index(token):

    #conn = sqlite3.connect(SURVEY_DB_FILE)
    #conn.text_factory = str
    #c = conn.cursor()
    # check that token exists
    # get list of receivers
    conn = boto.dynamodb2.connect_to_region(
        'us-west-1',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    def _authenticate(token):
        users = Table('survey2_users', connection=conn)
        return users.get_item(token=token)
        #c.execute("SELECT * FROM users WHERE token = ?", (token,))
        #return c.fetchone()

    def _submited(token):
        results = Table('survey2_results', connection=conn)
        return results.get_item(token=token)
        #c.execute("SELECT * FROM result WHERE token = ?", (token,))
        #return c.fetchone()

    if _authenticate(token) and not _submited(token):
        #print token
        q1 = request.forms.get('delivery')
        q2 = request.forms.get('feeling')
        comment = request.forms.get('comment')
        # CHANGE FOR AWS
        results = Table('survey2_results', connection=conn)
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
        raise error



    return template(codecs.open(BASEDIR + 'templates/base.html', 'r', 'utf-8').read(),        
    	            msg='Thank you!', state='success')



if __name__ == '__main__':
    run(host='localhost', port=8080)
