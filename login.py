# import python libraries
import json
import sqlite3
from flask import session, jsonify

from issue_tracker import app

from db import get_db

def login_user(username, password_hash):
    # initialise connection
    db = get_db()
    cursor = db.cursor()

    correct_hash = cursor.execute("""
        SELECT password_hash
        FROM users
        WHERE username == ?
        ;
        """, [username]).fetchone()
    
    if password_hash == correct_hash[0]:
        session['username'] = username
        return True
    else:
        return False

def get_hash(username):
    #initialise connection
    db = get_db()
    cursor = db.cursor()

    password_hash = cursor.execute("""
        SELECT password_hash
        FROM users
        WHERE username == ?
        ;
        """, [username]).fetchone()
    if password_hash is not None:
        return password_hash
    else:
        return ''
