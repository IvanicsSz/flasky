from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, SelectField, PasswordField, IntegerField
from flask_wtf.html5 import NumberInput
from wtforms.validators import DataRequired, Length
from wtforms import validators

class NameForm(Form):
    name = StringField(u'Story Title', validators=[DataRequired()])
    story = TextAreaField(u'User Story', validators=[DataRequired()])
    criteria = TextAreaField(u'Acceptance Criteria', validators=[DataRequired()])
    business = IntegerField(u'Business Value', widget=NumberInput(step=100)) # widget=NumberInput(u'Business Value', [validators.NumberRange(min=100, max=1500)]), )
    estimation = IntegerField(u'Estimation', widget=NumberInput(step=0.5))
    status = SelectField(u'Status', choices=[('planning', 'Planning'), ('to_do', 'To Do'), ('in_progress', 'In Progress'), ('review', 'Review'), ('done', 'Done')])
    submit = SubmitField('Submit')
    IntegerField(widget=NumberInput())

class LoginForm(Form):
    username = StringField(u'What is your user name?', validators=[DataRequired()])
    password = PasswordField(u'What is your password?', validators=[DataRequired()])
    submit = SubmitField('Submit')