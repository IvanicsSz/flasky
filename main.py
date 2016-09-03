from flask import Flask, render_template, session, redirect, url_for, g, request, flash, views
from functools import wraps
from datetime import datetime
from peewee import *
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from forms import *
from models import *
from user import *


# g.user = None
secret = os.urandom(24)
DEBUG = True
SECRET_KEY = secret
USERNAME = 'admin'
PASSWORD = 'default'
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'hard to guess'
app.config.from_object(__name__)


def connect_db():
    try:
        con = connect(user=User.db_username, host='localhost', password=User.db_passworld, port=5432)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute('CREATE DATABASE ' + User.db_name)
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



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@app.route("/list")
@login_required
def index():
    stories = Story.select()
    print(g.__dict__)
    return render_template('list.html', query=stories)


@app.route("/story/<int:story_id>", methods=["GET", "POST"])
def one_story(story_id):
    stori = Story.get_story_id(story_id)
    if request.method == "POST":
        stori.story_title = request.form['story_title']
        stori.user_title = request.form['story_content']
        stori.acceptance_criteria = request.form['acceptance_criteria']
        stori.business_value = int(request.form['business_value'])
        stori.estimation = request.form['estimation']
        stori.status = request.form['status']
        stori.data = datetime.utcnow()
        stori.save()
        flash("Your {}. story has been edited".format(story_id))
        return redirect(url_for('index'))

    return render_template('form.html', query=stori)


@app.route('/story', methods=['GET', 'POST'])
def story():
    # print(form.validate_on_submit())
    if request.method == "POST":  # if form.validate_on_submit():

        new = Story.create(story_title=request.form['story_title'], user_title=request.form['story_content'],
                           acceptance_criteria=request.form['acceptance_criteria'],
                           business_value=int(request.form['business_value']),
                           estimation=request.form['estimation'], status=request.form['status'], date=datetime.utcnow())
        new.save()
        return redirect(url_for('index'))
    return render_template('form.html', query="")



# @app.route('/login', methods=['GET', 'POST'])

class Login(views.MethodView):

    def get(self):
        error = None
        form = LoginForm()
        flash("Let's log in username: admin password: default")
        return render_template('user.html', form=form, error=error)
# def login():
    def post(self):
        if request.method == 'POST':
            if request.form['username'] != app.config['USERNAME']:
                error = 'Invalid username'
            elif request.form['password'] != app.config['PASSWORD']:
                error = 'Invalid password'
            else:
                session['logged_in'] = True
                session['username'] = request.form['username']
                # print(session['username'])

                flash("You are logged in {}".format(request.form['username']))
                return redirect(url_for('index'))


@app.route("/del/<int:story_id>")
def delete(story_id):
    remove = Story.get_story_id(story_id)
    remove.delete_instance()
    flash('You have deleted the {} story!'.format(story_id))
    return redirect(url_for('index'))


# @app.route('/logout')
class Logout(views.MethodView):
    def get(self):
        session.pop('logged_in', None)
        session.pop('username', None)
        # flash('You were logged out')
        return 'You were logged out'


app.add_url_rule('/login',
                 view_func=Login.as_view('login'),
                 methods=["GET", "POST"])

app.add_url_rule('/logout',
                 view_func=Logout.as_view('logout'))






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
