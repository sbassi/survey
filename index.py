from bottle import (post, run, template, request, 
	                get, static_file, template)
import sqlite3
import settings
import codecs

#from jinja2 import Template

SURVEY_DB_FILE = settings.SURVEY_DB_FILE
BASEDIR = settings.BASEDIR

@get('/survey2.png')
def images():
    return static_file('survey2.png', root='')

@get('/')
def home():
    return template(codecs.open(BASEDIR + 'templates/base.html', 'r', 'utf-8').read(),        
    	            msg='Server for internal survey', state='default')


@post('/surveypost/<token>')
def index(token):

    conn = sqlite3.connect(SURVEY_DB_FILE)
    conn.text_factory = str
    c = conn.cursor()
    # check that token exists

    def _authenticate(token):
        c.execute("SELECT * FROM users WHERE token = ?", (token,))
        return c.fetchone()

    def _submited(token):
        c.execute("SELECT * FROM result WHERE token = ?", (token,))
        return c.fetchone()

    if _authenticate(token) and not _submited(token):
        #print token
        q1 = request.forms.get('delivery')
        q2 = request.forms.get('feeling')
        comment = request.forms.get('comment')
        c.execute("INSERT INTO result VALUES (?,?,?,?)", 
                 (token,q1,q2,comment))
        conn.commit()
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
