
import flask.ext.wtf
import wtforms


class Edit(flask.ext.wtf.Form):
    """The form for editing the orgchart"""
    test_data = wtforms.StringField('ignored')
