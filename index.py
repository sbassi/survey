from bottle import post, run, template, request
import sqlite3
import settings

SURVEY_DB_FILE = settings.SURVEY_DB_FILE



@post('/surveypost/<token>')
def index(token):

    conn = sqlite3.connect(SURVEY_DB_FILE)
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
        return 'Survey already submited'

    else:
        raise error



    #return template('Thank you!')
    return 'Thank you!'







run(host='localhost', port=8080)
