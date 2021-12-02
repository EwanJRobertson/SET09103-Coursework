import sqlite3
from database import get_db

db = get_db()
cursor = db.cursor()

# create new user
def new_user(options):
    cursor.execute("""
        INSERT INTO users VALUES(?,?)
        ;
    """, options)
    db.commit()
    return None

# get all projects that a user is a part of
def get_projects(user_id):
    return cursor.execute("""
        SELECT project.project_id, project.title, project.version 
        FROM projects JOIN projects_users_link ON projects.project_id = project_users_link.project_id
        WHERE user_id == ? 
        GROUP BY project.project_id
        ;
    """, options)

# create new project
def new_project(options):
    cursor.execute("""
        INSERT INTO projects 
        VALUES(?, ?, ?)
        ;
    """, options)
    db.commit()
    return None

# get project indo
def get_project_info(project_id):
    return cursor.execute("""
        SELECT * 
        FROM projects
        WHERE project_id == ?
        ;
    """, options)

# get issues associated with project
def get_project_issues(project_id):
    return cursor.execute("""
        SELECT *
        FROM issues
        WHERE project_id == ?
        ;
    """, options)
    return None

# edit existing project
def edit_project(options):
    str = ""
    for row in cursor.execute("""
        SELECT *
        FROM projects
        WHERE project_id = ?
        ;
    """, options):
        str = row
    
    current = str[1, len(str) -2].split(", ")
    new = []
    for option in options:
        if option != "":
            new.append(option)
        else:
            new.append[current[len(new)]]
    
    cursor.execute("""
        DELETE *
        FROM projects
        WHERE project_id = ?
        ;
    """, options)
    cursor.commit()

    cursor.execute("""
        INSERT INTO projects
        VALUES(?, ?, ?)
        ;
        """, options)
    cursor.commit()

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
