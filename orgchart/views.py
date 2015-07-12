from __future__ import print_function

import flask
import os

from flask import request

from . import constants
from . import flask_app


@flask_app.route('/')
@flask_app.route('/index')
def index():
    return "Hello, World!"


@flask_app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.form:
        print(request.form)
        return flask.redirect('/view')
    else:
        graph = flask_app.config[constants.GRAPH]
        people = sorted(graph.list_people())
        tags = {
            person: graph.list_person_tags(person)
            for person in people
        }
        links = {
            from_person: {
                to_person: graph.list_links_between(from_person, to_person)
                for to_person in people
            }
            for from_person in people
        }
        return flask.render_template(
            'edit.html',
            people_list=people,
            tag_map=tags,
            link_map=links)


@flask_app.route('/view')
def view():
    return flask.render_template(
        'view.html',
        jquery=flask_app.config[constants.JQUERY],
        jquery_mousewheel=flask_app.config[constants.JQUERY_MOUSEWHEEL],
        jquery_color=flask_app.config[constants.JQUERY_COLOR],
        jquery_graphviz_svg=flask_app.config[constants.JQUERY_GRAPHVIZ_SVG])


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
