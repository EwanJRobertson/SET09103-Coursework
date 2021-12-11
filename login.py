# import python libraries
import json
import sqlite3
from flask import session, jsonify

from issue_tracker import app

from db import get_db

def login(username, password_hash):
    # initialise connection
    db = get_db()
    cursor = db.cursor()

    correct_hash = cursor.execute("""
        SELECT password_hash
        FROM users
        WHERE username = ?
        ;
        """, [username]).fetchone()[0]
    
    if password_hash == correct_hash:
        session['username'] = username
        return jsonify(response = "Login attempt succeded.")
    else:
        return jsonify(response = "Login attempt failed.")