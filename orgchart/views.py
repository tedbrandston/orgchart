
import flask
import os

from . import constants
from . import flask_app
from . import forms


@flask_app.route('/')
@flask_app.route('/index')
def index():
    return "Hello, World!"


@flask_app.route('/edit', methods=['GET', 'POST'])
def edit():
    graph = flask_app.config[constants.GRAPH]
    form = forms.Edit()
    form.set_person_choices(graph.list_people())
    if form.validate_on_submit():
        graph.ensure_person_exists(form.add_person.data)
        graph.delete_person(form.delete_person.data)
        graph.tag_person(form.person_to_tag.data, form.add_tag.data)
        graph.untag_person(form.person_to_untag.data, form.remove_tag.data)
        graph.link_people(
            form.add_link_from.data,
            form.add_link_to.data,
            form.add_link.data)
        graph.delete_link(
            form.del_link_from.data,
            form.del_link_to.data,
            form.del_link.data)
        # I know, I probably shouldn't be writing to disk on every request,
        # it's not 'web scale', or even, perhaps, scalable to the < 10 people
        # I expect to use this at any given time. Probably I should push this
        # into some queue in a different thread.
        graph.save('no comment')
        return flask.redirect('/view')
    return flask.render_template('edit.html', form=form)


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
