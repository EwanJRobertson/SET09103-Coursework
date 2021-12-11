# import python libraries
from flask import Flask, g, redirect, render_template, request, session, url_for
import json

# define app
app = Flask(__name__)
app.secret_key = 'secret'

# import
import db_operations
from login import login_user

# login page
@app.route('/')
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_hash = request.form['password']
        if login_user(username, password_hash):
            return redirect('/user/' + username)
    else:
        return render_template('login.html', type="Login", login=True)

@app.route('/new-user', methods = ['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        if db_operations.new_user(request.form['username'], request.form['password']):
            return redirect('/user/' + request.form['username'])
        else:
            print()
    else:
        return render_template('login', type="New User", login=False)

@app.route('/user/<user>', methods = ['GET'])
def user(name):
    try:
        if session['username']:
            session_user = str[session['username']]
            if session_user != name:
                redirect('/user')
    except:
        redirect('/user')

#@app.route('/user/<user>/projects', methods = ['GET'])
#def projects(user):
#    try:
#        if session['username']:
#            if user == str(session['username']):
#                order = ""
#                try:
#                    if request.args.get('sort-by'):
#                        order = request.args.get('sort-by')
#                except:
#                    order = ""
#                return render_template('projects.html', projects = db_operations.get_projects(user, order).json['records'])
#    except:
#        return render_template('projects.html')
    
@app.route('/user/<user>/projects/<project>', methods = ['GET'])
def projects(user, project):
    try:
        if session['username']:
            print("2")
    except:
        print("3")

@app.route('/user/<user>/projects/<project>/<issue_id>', methods = ['GET', 'POST'])
def issue(user, project, issue_id):
    print("1")

@app.route('/error', methods = ['GET'])
def error():
    print("bridge closed")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
