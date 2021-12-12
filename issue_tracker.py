# import python libraries
from flask import Flask, g, redirect, render_template, request, session, url_for
import json
import bcrypt

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
        password_hash = bcrypt.haspw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        if login_user(username, password_hash):
            return redirect('/' + username)
        else:
            return render_template('login.html', type="Login", login=True)
    else:
        session.pop('username', None)
        return render_template('login.html', type="Login", login=True)

@app.route('/new-user', methods = ['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        username = request.form['username']
        password_hash = bcrypt.haspw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        if db_operations.new_user(username, password_hash):
            login_user(username, password_hash)
            return redirect('/' + request.form['username'])
        else:
            return render_template('login.html', type="New User", login=False)
    else:
        return render_template('login.html', type="New User", login=False)

@app.route('/<username>', methods = ['GET'])
def user(username):
    try:
        if username != str(session['username']):
            return redirect('/login.html')
        else:
            return render_template('user.html')
    except:
        return redirect('/login.html')

@app.route('/<username>/projects', methods = ['GET', 'POST'])
def projects(username):
    if request.method == 'POST':
        return 1
    else:
        try:
            if username != str(session['username']):
                return redirect('/login')
            else:
                if request.args.get('action') == 'view':
                    return render_template('list_view.html', type='user', action = 'view', records = db_operations.get_projects(username))
                else:
                    return render_template('info-view.html', type='project', action = 'new')
        except:
            return redirect('/login')

@app.route('/<username>/<project_id>', methods = ['GET', 'POST'])
def projects(username, project_id):
    if request.method == 'POST':
        print(1)
    else:
        try:
            if username != str(session['username']) or not db_operations.is_user_linked(username, project_id):
                return redirect('/' + str(session['username']))
            else:
                try:
                    order = request.args.get('order')
                    projects = db_operations.get_project_issues(project_id, order, username)
                    info = db_operations.get_project_info(project_id, username)
                    if request.args.get('action') == 'view':
                        return render_template('list_view.html', type = 'project', action = 'view', records = projects, info = info)
                    elif request.args.get('action') == 'new':
                        return render_template('list_view.html', type = 'project', action = 'new', records = projects, info = info)
                    else:
                        return render_template('list_view.html', type = 'project', action = 'edit', records = projects, info = info)
                except:
                    return redirect('/' + str(session['username']))
        except:
            return redirect('/login')

@app.route('/<username>/<project_id>/<issue_id>', methods = ['GET', 'POST'])
def issue(username, project_id, issue_id):
    print("1")

@app.route('/error', methods = ['GET'])
def error():
    print("bridge closed")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
