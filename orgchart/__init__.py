
import flask

flask_app = flask.Flask(__name__)
flask_app.config.from_envvar('ORGCHART_FLASK_CONFIG')

from . import constants
constants.set_defaults(config)

from . import forms
from . import graph
from . import views
