# import python flask library
from flask import Flask, g, redirect, render_template, request, session, url_for
import json

# define app
app = Flask(__name__)
app.secret_key = 'secret'

# import database
import db_operations

# login page
@app.route('/')
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['name'] = "Ewan"
        return "Post"
    else:
        try:
            if session['username']:
                user = str[session['username']]
                redirect('/user/' + user)
        except:
            session['name'] = "Ewan"
            return "Get"

@app.route('/user', methods = ['GET', 'POST'])
def users():
    return "User"

@app.route('/user/<user>', methods = ['GET'])
def user(name):
    try:
        if session['username']:
            session_user = str[session['username']]
            if session_user != name:
                redirect('/user')
    except:
        redirect('/user')

if __name__ == "__main__":
    pp.run(host="0.0.0.0", debug=True)
