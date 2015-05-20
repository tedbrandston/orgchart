
import flask.ext.wtf
import wtforms


class Edit(flask.ext.wtf.Form):
    """The form for editing the orgchart"""
    node_a = wtforms.StringField()
    node_b = wtforms.StringField()
    edge = wtforms.StringField()
