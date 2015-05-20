
import flask
import os

from . import constants
from . import flask_app
from . import forms
from . import graph


@flask_app.route('/')
@flask_app.route('/index')
def index():
    return "Hello, World!"


@flask_app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = forms.Edit()
    if form.validate_on_submit():
        # I know, I probably shouldn't be writing to disk on every request,
        # it's not 'web scale', or even, perhaps, scalable to the < 10 people
        # I expect to use this at any given time. Probably I should push this
        # into some queue in a different thread.
        graph.write_to_dotfile(
            flask_app.config[constants.GRAPH],
            flask_app.config[constants.DOTFILE])
        graph.generate_svg(
            flask_app.config[constants.DOTFILE],
            flask_app.config[constants.SVG])
        return flask.redirect('/view')
    return flask.render_template('edit.html', form=form)


@flask_app.route('/view')
def view():
    return flask.render_template('view.html')

@flask_app.route('/orgchart.dot')
def dot():
    return flask.send_file(os.path.join(
        os.pardir,
        flask_app.config[constants.DOTFILE]))

@flask_app.route('/orgchart.svg')
def svg():
    return flask.send_file(os.path.join(
        os.pardir,
        flask_app.config[constants.SVG]))
