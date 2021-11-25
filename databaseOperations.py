import sqlite3
from database import get_db

# create new user
def new_user(db, options):
    db.cursor().execute("INSERT INTO users VALUES(?,?);", options)
    db.commit()
    return None

# submit password and username, attempt login
def login(db, username, password):
    return None

# get all projects that a user is a part of
def get_projects(db, user_id):
#   return db.cursor.execute("SELECT project.project_id, project.title, project.version FROM projects JOIN projects_users_link WHERE user_id == '%{user_id}%' GROUP BY project.project_id;".format=(user_id = user_id))
    return None

# create new project
def new_project(options):
    get_db().cursor().execute('INSERT INTO projects VALUES(?, ?, ?);', options)
    get_db().commit()
    return None

# get project indo
def get_project_info(project_id):
    return get_db().cursor().execute('SELECT * FROM projects;')

# get issues associated with project
def get_project_issues(db, project_id):
    return None

# edit existing project
def edit_project(db, project_id, options):
    return None

# add user to project
def assign_project(db, options):
    return None

# leave project
def leave_project(db, user_id, project_id):
    return None

# create new issue
def create_issue(db, project_id, options):
    return None

# get issue
def get_issue(db, project, issue_id):
    return None

# edit issue
def edit_issue(db, project_id, issue_id, options):
    return None

# delete issue
def delete_issue(db, project_id, issue_id):
    return None
