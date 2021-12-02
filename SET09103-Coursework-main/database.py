# import sqlite3 library
import sqlite3
from flask import g

from appl import app

# define location of database
db_location = 'var/issue_tracker.db'

# get instance of the database
def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = sqlite3.connect(db_location)
        g.db = db
    return db

# close database
@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# initialise database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('static/sql/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
