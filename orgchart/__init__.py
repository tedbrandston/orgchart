
import flask

flask_app = flask.Flask(__name__)
flask_app.config.from_envvar('ORGCHART_FLASK_CONFIG')

from . import views
from . import graph
