"""
    Forms
    ~~~~~
"""
from flask_wtf import Form
from wtforms import BooleanField
from wtforms import TextField
from wtforms import DateField
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import PasswordField
from wtforms.validators import InputRequired
from wtforms.validators import ValidationError
import os.path, time

from wiki.core import clean_url
from wiki.web import current_wiki
from wiki.web import current_users


class URLForm(Form):
    url = TextField('', [InputRequired()])

    def validate_url(form, field):
        if current_wiki.exists(field.data):
            raise ValidationError('The URL "%s" exists already.' % field.data)

    def clean_url(self, url):
        return clean_url(url)



class SearchForm(Form):
    term = TextField('', [InputRequired()])
    ignore_case = BooleanField(
        description='Ignore Case',
        # FIXME: default is not correctly populated
        default=True)
    date_option = DateField(
        description='Date'
    )
    keyword = StringField(
        description='Keyword'
    )


class SearchFormDate(Form):
    date_term = TextField('', [InputRequired()])
    date_option = DateField(
        description='Date'
    )


class EditorForm(Form):
    title = TextField('', [InputRequired()])
    body = TextAreaField('', [InputRequired()])
    tags = TextField('')


class LoginForm(Form):
    name = TextField('', [InputRequired()])
    password = PasswordField('', [InputRequired()])

    def validate_name(form, field):
        user = current_users.get_user(field.data)
        if not user:
            raise ValidationError('This username does not exist.')

    def validate_password(form, field):
        user = current_users.get_user(form.name.data)
        if not user:
            return
        if not user.check_password(field.data):
            raise ValidationError('Username and password do not match.')
