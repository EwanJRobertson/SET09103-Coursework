# import python libraries
import json
import sqlite3
from flask import session, jsonify

from issue_tracker.issue_tracker import app

from issue_tracker.db import get_db

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
        session['init']='Test'
        session['username'] = username
        return True
    else:
        return False

def get_hash(username):
    #initialise connection
    db = get_db()
    cursor = db.cursor()

    return cursor.execute("""
        SELECT password_hash
        FROM users
        WHERE username == ?
        ;
        """, [username]).fetchone()[0]

def change_password(username, old_password, new_password):
    #initialise connection
    db = get_db()
    cursor = db.cursor()

    if login_user(username, old_password):
        cursor.execute("""
            UPDATE users
            SET password_hash = ?
            WHERE username = ?
            ;
            """, [new_password, username])
        cursor.commit()
        return True
    return False
