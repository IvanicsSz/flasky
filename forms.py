from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, validators
from wtforms.validators import DataRequired, Length

class NameForm(Form):
    name = StringField(u'What is your name?', validators=[DataRequired()])
    story = TextAreaField(u'Second message', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(Form):
    username = StringField(u'What is your user name?', validators=[DataRequired()])
    password = StringField(u'What is your password?', validators=[DataRequired()])
    submit = SubmitField('Submit')