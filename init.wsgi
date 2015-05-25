import os
import sys

import bottle

sys.path = ['/var/www/survey/htdocs/'] + sys.path
os.chdir(os.path.dirname(__file__))

import index

# ... build or import your bottle application here ...
# Do NOT use bottle.run() with mod_wsgi
application = bottle.default_app()