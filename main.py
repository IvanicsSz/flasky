import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/', methods=["GET", "POST"])
def show_entries():

    if request.method == "POST":
        data = request.form
        db = get_db()
        print(data['user_name'], data['story'])
        db.execute('insert into entries (user, story) values (?, ?)', [i for i in data.values()])
        db.commit()
        return render_template('username.html')
    return render_template('show_entries.html' )
    # return redirect(url_for('username'))

@app.route('/username', methods=["GET", "POST"])
def username():
    # data['user_name'] = request.form['user_name']
    # data['story'] = request.form['story']
    #
    db =get_db()

    if request.method == "POST":
        cur = db.execute('select id, user, story from entries where id={0} order by id desc'.format(request.form['id']))
        entries = cur.fetchall()
        return render_template('username.html', entries=entries)

    else:
        cur = db.execute('select id, user, story from entries order by id desc')
        entries = cur.fetchall()
        return render_template('username.html', entries=entries)
    # user = name

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# Query runner
def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    db.commit()
    cur.close()

    # return (rv if rv else None) if one else rv
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


if __name__ == '__main__':
    with app.app_context():
        # init_db()
        connect_db()
        get_db()
        app.run(debug=True)
