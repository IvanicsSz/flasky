from flask import Flask, render_template, session, redirect, url_for, g, request, flash, make_response
from datetime import datetime
from peewee import *
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
# from forms import *
from models import *

secret = os.urandom(24)
DEBUG = True
SECRET_KEY = 'ssshhhh'
USERNAME = 'admin'
PASSWORD = 'default'
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'hard to guess'
app.config.from_object(__name__)


def connect_db():
    try:
        dbname = 'story'
        con = connect(user='szilard', host='localhost', password='753951', port=5432)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute('CREATE DATABASE ' + dbname)
        cur.close()
        con.close()
    except:
        print("Database already exist")


@app.before_first_request
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'postgres_db'):
        g.postgres_db = connect_db()
        # db.connect()
        # db.drop_tables([Story], safe=True)
        db.create_tables([Story], safe=True)
    return g.postgres_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'postgres_db'):
        g.postgres_db.close()


@app.route("/")
@app.route("/list")
def index():
    stories = Story.select()
    return render_template('list.html', query=stories)


@app.route("/story/<int:story_id>", methods=["GET", "POST"])
def one_story(story_id):
    stori = Story.get(Story.id == story_id)
    if request.method == "POST":
        stori.story_title = request.form['story_title']
        stori.user_title = request.form['story_content']
        stori.acceptance_criteria = request.form['acceptance_criteria']
        stori.business_value = int(request.form['business_value'])
        stori.estimation = request.form['estimation']
        stori.status = request.form['status']
        stori.data = datetime.utcnow()
        stori.save()
        return redirect(url_for('index'))

    return render_template('form.html', query=stori)


@app.route('/story', methods=['GET', 'POST'])
def story():
    # print(form.validate_on_submit())
    if request.method == "POST":  # if form.validate_on_submit():

        print(request.form['estimation'])
        new = Story.create(story_title=request.form['story_title'], user_title=request.form['story_content'],
                           acceptance_criteria=request.form['acceptance_criteria'],
                           business_value=int(request.form['business_value']),
                           estimation=request.form['estimation'], status=request.form['status'], date=datetime.utcnow())
        new.save()
        print("print2")
        return redirect(url_for('index'))
    return render_template('form.html', query="")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    # form = LoginForm()
    flash("Let's log in")
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            return redirect(url_for('story'))
    return render_template('user.html', error=error)


@app.route("/del/<int:story_id>")
def delete(story_id):
    remove = Story.get(Story.id == story_id)
    remove.delete_instance()  # flash('You were logged out')
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    # flash('You were logged out')
    return 'You were logged out'


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
