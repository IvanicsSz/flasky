from flask import Flask, render_template, session, redirect, url_for, g, request,flash, make_response
from datetime import datetime
import codecs, json
from peewee import *
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, validators
from wtforms.validators import DataRequired, Length

secret = os.urandom(24)
DEBUG = True
SECRET_KEY = 'ssshhhh'
USERNAME = 'admin'
PASSWORD = 'default'
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'hard to guess'
app.config.from_object(__name__)


def connect_db():
    dbname = 'story'
    con = connect(user='szilard', host='localhost', password='753951', port=5432)
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute('CREATE DATABASE ' + dbname)
    cur.close()
    con.close()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'postgres_db'):
        g.postgres_db = connect_db()
    return g.postgres_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'postgres_db'):
        g.postgres_db.close()


db = PostgresqlDatabase('story', **{'user': "szilard", 'host': 'localhost', 'port': 5432,
                                    'password': '753951'})
db.connect()


class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = db


class Story(BaseModel):
    first_name = CharField()
    last_name = CharField()


# List the tables here what you want to create...
db.drop_tables([Story], safe=True)
db.create_tables([Story], safe=True)


class NameForm(Form):
    name = StringField(u'What is your name?', validators=[DataRequired()])
    story = TextAreaField(u'Second message', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(Form):
    username = StringField(u'What is your user name?', validators=[DataRequired()])
    password = StringField(u'What is your password?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    # print(form.validate_on_submit())
    if request.method == "POST":  # if form.validate_on_submit():
        session['name'] = form.name.data
        jani = Story.create(first_name=form.name.data, last_name="Jani")
        jani.save()
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    flash("Let's log in")
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('user.html', form=form, error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    # flash('You were logged out')
    return 'You were logged out'


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=datetime.utcnow())
# url_for('profile', name='John Doe')
# url_for('login', next='/')
# Inside templates you also have access
# to the request, session and g [1] objects
# as well as the get_flashed_messages() function.
# searchword = request.args.get('key', '')
# @app.errorhandler(404)
# def not_found(error):
#     resp = make_response(render_template('error.html'), 404)
#     resp.headers['X-Something'] = 'A value'
#     return resp
if __name__ == '__main__':
    app.run(debug=True)
