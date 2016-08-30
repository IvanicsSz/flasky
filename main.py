from flask import Flask, render_template, session, redirect, url_for
from datetime import datetime
from flask_peewee.db import Database

from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, validators
from wtforms.validators import DataRequired, Length

DATABASE = {
    'name': 'example.db',
    'engine': 'peewee.SqliteDatabase',
}
DEBUG = True
SECRET_KEY = 'ssshhhh'
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'hard to guess'
app.config.from_object(__name__)

# some changes
db = Database(app)


class NameForm(Form):
    name = StringField(u'What is your name?', validators=[DataRequired()])
    story = TextAreaField(u'Second message', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(Form):
    login = StringField(u'What is your name?', validators=[DataRequired()])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    # print(form.validate_on_submit())
    if form.name.data:  # if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = session.get('name')
    return render_template('user.html', form=form, user=user)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=datetime.utcnow())


if __name__ == '__main__':
    app.run(debug=True)
