
# encuesta

# conexion a DB para token

from bottle import route, run, template

@route('/surveypost/<token>')
def index(name):
    # check that token exists

    if _authenticate(token):
        pass
    else:
        raise error



    return template('<b>Hello {{name}}</b>!', name=name)


def _authenticate(token):
    
    return true





run(host='localhost', port=8080)