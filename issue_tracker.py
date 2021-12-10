# import python flask library
from flask import Flask, g, redirect, render_template, request, session, url_for
import json

# define app
app = Flask(__name__)

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
            return "Get"

@app.route('/user', methods = ['GET', 'POST'])
def new_user():
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

@app.route('/user/<user>/projects', methods = ['GET'])
def projects(user):
    try:
        if session['username']:
            if user == str[session['username']]:
                return render_template('projects.html', db_operations.get_projects(user, request.GET.get('sort-by')))
    except:
        return "except"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
