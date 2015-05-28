
import flask.ext.wtf
import wtforms


class Edit(flask.ext.wtf.Form):
    """The form for editing the orgchart"""
    add_person = wtforms.StringField()
    delete_person = wtforms.SelectField('Person')
    add_tag = wtforms.StringField()
    person_to_tag = wtforms.SelectField('Person')
    remove_tag = wtforms.StringField()
    person_to_untag = wtforms.SelectField('Person')

    def set_person_choices(self, people):
        """
        This seems really strange to me, that I'm setting class-level
        stuff to different things, and just relying on the timing to
        make it work. Maybe I'm just misunderstanding this framework?

        Any SelectFields that need a list of people should appear here
        """
        pairs = zip(people, people)
        self.delete_person.choices = pairs
        self.person_to_tag.choices = pairs
        self.person_to_untag.choices = pairs
