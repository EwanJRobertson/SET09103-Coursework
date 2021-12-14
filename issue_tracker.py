# import python libraries
import configparser
import logging
import json
import bcrypt

from logging.handlers import RotatingFileHandler
from functools import wraps
from flask import Flask, g, redirect, render_template, request, session, url_for

# define app
app = Flask(__name__)
app.secret_key = 'secret'

# import operations
import db_operations
from login import change_password, login_user, get_hash

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

# login decorator
def requires_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if kwargs['username'] != session.get('username'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# is user linked to project decorator
def requires_assigned_to_project(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not db_operations.is_user_linked(kwargs['user'], kwargs['project_id']):
            return redirect(url_for('user', username = kwargs['user']))
        return f(*args, **kwargs)
    return decorated

# login page
@app.route('/')
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if get_hash(username) is None:
            return render_template('login.html', type = 'login')
        password_hash = bcrypt.hashpw(request.form['password'].encode('utf-8'), get_hash(username))
        app.logger.info('Log in attempt for user:' + username)
        if login_user(username, password_hash):
            return redirect(url_for('user', username = username))
        else:
            return render_template('login.html', type = 'login')

    else:
        session.pop('username', None)
        return render_template('login.html', type = 'login')

# new user
@app.route('/new-user', methods = ['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        username = request.form['username']
        password_hash = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        if db_operations.new_user(username, password_hash):
            login_user(username, password_hash)
            return redirect(url_for('user', username = username))
        else:
            return render_template('login.html', type = 'new user')

    else:
        return render_template('login.html', type = 'new user')

# user page
@app.route('/user/<username>', methods = ['GET', 'POST'])
@requires_login
def user(username):
    if request.method == 'POST':
        if username == request.form['username']:
            change_password(username, request.form['password'], bcrypt.hashpw(request.form['new_password'].encode('utf-8'), bcrypt.gensalt()))
        return redirect(url_for('user', username = username))

    else:
        try:
            if request.args['change-password'] == 'True':
                return render_template('login.html', type = 'edit')
        except:
                return render_template('user.html', username = username)

# user projects
@app.route('/user/<username>/projects', methods = ['GET', 'POST'])
@requires_login
def projects(username):
    if request.method == 'POST':
        title = request.form['title']
        version = request.form['version']
        db_operations.new_project(title, version, username)
        return redirect(url_for('projects', username = username))

    else:
        try:
            if request.args and request.args.get('action') == 'new':
                return render_template('item.html', username = username, type = 'project', action = 'new' )
            else:
                return render_template('list_view.html', username = username, type = 'user', action = 'view', records = db_operations.get_projects(username, '', '').json['records'])
        except Exception as e:
            print(e)
            return redirect(url_for('login'))

# project page
@app.route('/user/<username>/<project_id>', methods = ['GET','PATCH', 'POST'])
@requires_login
@requires_assigned_to_project
def project(username, project_id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        type_of_issue = request.form['type_of_issue']
        version_introduced = request.form['version_introduced']
        priority_level = request.form['priority_level']
        status = request.form['status']
        db_operations.new_issue(project_id, title, description, type_of_issue, version_introduced, username, priority_level, status)
        return redirect(url_for('project', username = username, project_id = project_id))
    
    elif request.method == 'PATCH':
        title = request.form['title']
        version = request.form['version']
        db_operations.edit_project(project_id, title, version)
        return redirect(url_for('project', username = username, project_id = project_id))
    
    else:
        try:
            order = request.args.get('order')
            info = db_operations.get_project_info(project_id, username)
            if info is None:
                return redirect(url_for('user', username = username))
            projects = db_operations.get_project_issues(project_id, order, username)
            if request.args.get('action') == 'view':
                return render_template('list_view.html', type = 'project', action = 'view', records = projects, info = info)
            elif request.args.get('action') == 'new':
                return render_template('item.html', type = 'issue', action = 'new')
            else:
                return render_template('item.html', type = 'project', action = 'edit', record = info)
        except:
            return redirect(url_for('user', username = username))

# issue page
@app.route('/user/<username>/<project_id>/<issue_id>', methods = ['GET', 'PATCH'])
@requires_login
@requires_assigned_to_project
def issue(username, project_id, issue_id):
    if request.method == 'PATCH':
        title = request.form['title']
        description = request.form['description']
        priority_level = request.form['priority_level']
        status = request.form['status']
        db_operations.edit_issue(project_id, issue_id, title, description, type_of_issue, version_introduced, username, priority_level, status)
        return redirect(url_for('issue', username = username, project_id = project_id, issue_id = issue_id))

    else:
        try:
            issue = db_operations.get_issue(project_id, issue_id, username)
            if request.args.get('action') == 'view':
                return render_template('item.html', type = 'project', action = 'view', record = issue)
            else:
                return render_template('item.html', type = 'project', action = 'edit', record = issue)
        except:
            return redirect(url_for('user', username = username))

# error page
@app.route('/error', methods = ['GET'])
def error():
    print('bridge closed')

if __name__ == "__main__":
    init(app)
    logs(app)
    app.run(host = app.config['ip_address'],
            port = int(app.config['port']))
