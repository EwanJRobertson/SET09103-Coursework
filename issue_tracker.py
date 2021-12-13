# import python libraries
import configparser
import logging
import json
import bcrypt

from logging.handlers import RotatingFileHandler
from flask import Flask, g, redirect, render_template, request, session, url_for

# define app
app = Flask(__name__)
app.secret_key = 'secret'

# import operations
import db_operations
from login import login_user, get_hash

# initialise app
def init(app):
    config = configparser.ConfigParser()
    try:
        config_location = 'etc/defaults.cfg'
        config.read(config_location)

        app.config['DEBUG'] = config.get('config', 'debug')
        app.config['ip_address'] = config.get('config', 'ip_address')
        app.config['port'] = config.get('config', 'port')
        app.config['url'] = config.get('config', 'url')
        app.config['secret_key'] = config.get('config', 'secret_key')

        app.config['log_file'] = config.get('logging', 'name')
        app.config['log_location'] = config.get('logging', 'location')
        app.config['log_level'] = config.get('logging', 'level')
    except:
        print('Could not read config file from ' + config_location)

# initialise logging
def logs(app):
    log_pathname = app.config['log_location'] + app.config['log_file']
    file_handler = RotatingFileHandler(log_pathname, maxBytes = 1024 * 1024 * 10, backupCount = 1024)
    file_handler.setLevel(app.config['log_level'])
    formatter = logging.Formatter('%(levelname)s | %(asctime)s | %(module)s | %(funcName)s | %(message)s')
    file_handler.setFormatter(formatter)
    app.logger.setLevel(app.config['log_level'])
    app.logger.addHandler(file_handler)

# login page
@app.route('/')
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_hash = bcrypt.hashpw(request.form['password'].encode('utf-8'), get_hash(username).encode('utf-8'))
        app.logger.info('Log in attempt for user:' + username)
        if login_user(username, password_hash):
            return redirect('/' + username)
        else:
            return render_template('login.html', type = "Login", login = True)
    else:
        session.pop('username', None)
        return render_template('login.html', type = "Login", login = True)

@app.route('/new-user', methods = ['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        username = request.form['username']
        password_hash = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
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
def project(username, project_id):
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
                        return render_template('.html', type = 'project', action = 'new')
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
    init(app)
    logs(app)
    app.run(host = app.config['ip_address'],
            port = int(app.config['port']))
