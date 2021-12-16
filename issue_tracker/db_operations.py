# import sqlite3
import sqlite3

# import jsonify to format return values
from flask import jsonify
import json

# import get db function to allow the getting of a connection to the database
from issue_tracker.db import get_db

# create new user
def new_user(username, password_hash):
    # initialise connection
    db = get_db()
    cursor = db.cursor()

    # check username provided is unique
    for row in cursor.execute("""
        SELECT username 
        FROM users
        ;
        """):
        if row[0] == username:
            return False

    # insert new user into database
    cursor.execute("""
        INSERT INTO users 
        VALUES(?,?)
        ;
        """, [username, password_hash])
    db.commit()
    return True

# get all projects that a user is a part of
def get_projects(username, search):
    # initialise connection
    db = get_db()
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    # execute query
    query_results = cursor.execute("""
        SELECT projects.project_id, projects.title, projects.version 
        FROM projects 
        JOIN users_projects_link 
            ON projects.project_id = users_projects_link.project_id
        WHERE username == ?
            AND title LIKE ?
        ;
        """, [username, search + '%']).fetchall()

    # return json objects
    return jsonify(records = json.dumps([dict(row) for row in query_results]))

# create new project
def new_project(title, version, username):
    # initialise connection
    db = get_db()
    cursor = db.cursor()

    # get next unique project id value
    project_id = 0
    for row in cursor.execute("""
        SELECT 1 
        FROM projects
        ;
        """):
        project_id += 1

    # insert new project into database
    cursor.execute("""
        INSERT INTO projects 
        VALUES(?, ?, ?)
        ;
        """, [project_id, title, version])
    db.commit()

    # assign initial user to project
    assign_project(username, project_id)
    return jsonify(response ='project added')

# get project info
def get_project_info(project_id, username):
    # initialise connection
    db = get_db()
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    # ensure project id is an integer
    try:
        project_id = int(project_id)
    except:
        return None

    # check user is linked to project
    if cursor.execute("""
        SELECT 1
        FROM users_projects_link
        WHERE username == ?
            AND project_id == ?
        ;
        """, [username, project_id]).fetchall() is []:
        return None

    # execute query
    query_results = cursor.execute("""
        SELECT * 
        FROM projects
        WHERE project_id == ?
        ;
        """, [project_id]).fetchall()
    
    # return json object
    return jsonify(records = json.dumps([dict(row) for row in query_results]))

# get projects users
def get_project_users(project_id, username):
    # initialise connection
    db = get_db()
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    # check project id is an integer
    try:
        project_id = int(project_id)
    except:
        return jsonify(response ='project ID must be an integer')

    # check user is linked to project
    if cursor.execute("""
        SELECT 1
        FROM users_projects_link
        WHERE username == ?
            AND project_id == ?
        ;
        """, [username, project_id]).fetchall() is []:
        return jsonify(response ='user is not on this project')

    # execute query and return results
    query_results = cursor.execute("""
        SELECT username 
        FROM users_projects_link
        WHERE project_id == ?
        ;
        """, [project_id]).fetchall()
    return jsonify(records = json.dumps([dict(row) for row in query_results]))

# is user on project
def is_user_linked(username, project_id):
    # initialise connection
    db = get_db()
    cursor = db.cursor()

    if cursor.execute("""
        SELECT 1
        FROM users_projects_link
        WHERE username == ?
            AND project_id == ?
        ;
        """, [username, project_id]).fetchall() is not []:
        return True
    return False

# get issues associated with project
def get_project_issues(project_id, search, username):
    # initialise connection
    db = get_db()
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    # check project id is an integer
    try:
        project_id = int(project_id)
    except:
        return jsonify(response ='project ID must be an integer')
    
    # check user is linked to project
    if cursor.execute("""
        SELECT 1
        FROM users_projects_link
        WHERE username == ?
            AND project_id == ?
        ;
        """, [username, project_id]).fetchall() is []:
        return jsonify(response ='user is not on this project')
    
    # execute query and return results
    query_results = cursor.execute("""
        SELECT *
        FROM issues
        WHERE project_id == ?
            AND title LIKE ?
        ;
        """, [project_id, search + '%']).fetchall()
    
    return jsonify(records = json.dumps([dict(row) for row in query_results]))

# add user to project
def assign_project(username, project_id):
    # initalise connection
    db = get_db()
    cursor = db.cursor()

    # check username is valid
    if cursor.execute("""
        SELECT 1 
        FROM users
        WHERE username == ?
        ;
        """, [username]).fetchall() is []:
        return jsonify(response = 'username is not valid')
    
    # check project is valid
    if cursor.execute("""
        SELECT project_id
        FROM projects
        WHERE project_id == ?
        ;
        """, [project_id]).fetchall() is []:
        return jsonify(response ='project is not valid')
    
    # check project id is an integer
    if not isinstance(project_id, int):
        return jsonify(response = 'project ID must be an integer')
    
    # check user is not already linked to project
    if cursor.execute("""
        SELECT 1
        FROM users_projects_link
        WHERE username == ?
            AND project_id == ?
        ;
        """, [username, project_id]).fetchall() != []:
        return jsonify(response = 'user is already linked to project')

    # insert new link between user and project
    cursor.execute("""
        INSERT INTO users_projects_link
        VALUES(?,?)
        ;
        """, [username, project_id])
    db.commit()
    return jsonify(response ='user linked to project')

# leave project
def leave_project(username, project_id):
    # initalise connection
    db = get_db()
    cursor = db.cursor()

    # check username is valid
    if cursor.execute("""
        SELECT 1
        FROM users
        WHERE username == ?
        ;
        """, [username]).fetchall() == []:
        return jsonify(response ='username is not valid')

    # check project id is an integer
    try:
        project_id = int(project_id)
    except:
        return jsonify(response ='project ID must be an integer')

    # remove user from any issues they are assigned on the project
    for row in cursor.execute("""
        SELECT *
        FROM issues
        WHERE username == ? 
            AND project_id == ?
        ;
        """, [username, project_id]):
        new = list(row)
        new[7] = ''
        cursor.execute("""
            UPDATE issues
            SET title = ?
                AND description = ?
                AND type_of_issue = ?
                AND date_last_updated = ?
                AND version_introduced = ?
                AND username = ?
                AND priority_level = ?
                AND status = ?
            WHERE project_id == ?
                AND issue_id == ?
            ;
            """, [new[2], new[3], new[4], new[5], new[6], new[7], new[8], new[9], new[0], new[1]])
        db.commit()
    
    # remove user project link
    cursor.execute("""
        DELETE FROM users_projects_link
        WHERE username == ?
            AND project_id == ?
        ;
        """, [username, project_id])
    db.commit()

# create new issue
def new_issue(project_id, title, description, type_of_issue, version_introduced, username, priority_level):
    # initalise connection
    db = get_db()
    cursor = db.cursor()

    # check project id is an integer
    try:
        project_id = int(project_id)
    except:
        return jsonify(response ='project ID must be an integer')
    
    # check priority level is empty string or an integer
    try:
        priority_level = int(priority_level)
    except:
        if priority_level != '':
            return jsonify(response ='priority level must be an empty string or an integer')
    
    # check project exists
    if cursor.execute("""
        SELECT 1
        FROM projects
        WHERE project_id == ?
        ;
        """, [project_id]).fetchall() is []:
        return jsonify(response ='project does not exist')
    
    # check user is linked to project
    if cursor.execute("""
        SELECT 1
        FROM users_projects_link
        WHERE username == ?
            AND project_id == ?
        ;
        """, [username, project_id]).fetchall() is []:
        return jsonify(response ='user is not on this project')

    # get next unique issue id value for project
    issue_id = 0
    for row in cursor.execute("""
        SELECT 1 
        FROM issues
        WHERE project_id == ?
        ;
        """, [project_id]):
        issue_id += 1
    
    # function to get date from system
    from datetime import datetime
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # insert new issue into database
    cursor.execute("""
        INSERT INTO issues
        VALUES(?,?,?,?,?,?,?,?,?,'backlog')
        ;
        """, [project_id, issue_id, title, description, type_of_issue, date, version_introduced, username, priority_level])
    db.commit()

# get issue
def get_issue(project_id, issue_id, username):
    # initalise connection
    db = get_db()
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    # check user is linked with project
    if cursor.execute("""
        SELECT 1
        FROM users_projects_link
        WHERE username == ?
            AND project_id == ?
        ;
        """, [username, project_id]).fetchall() is []:
        return jsonify(response ='user is not on this project')

    # get issue
    query_results = cursor.execute("""
        SELECT *
        FROM issues
        WHERE project_id == ?
            AND issue_id == ?
        ;
        """, [project_id, issue_id])
    return jsonify(record = json.dumps([dict(row) for row in query_results]))

# edit issue
def edit_issue(project_id, issue_id, title, description, type_of_issue, version_introduced, username, priority_level, status):
    # initalise connection
    db = get_db()
    cursor = db.cursor()

    # check project id is an integer
    try:
        project_id = int(project_id)
    except:
        return jsonify(response ='project ID must be an integer')

    # check user is linked to project
    if cursor.execute("""
        SELECT 1
        FROM users_projects_link
        WHERE username == ?
            AND project_id == ?
        ;
        """, [username, project_id]) is None:
        return jsonify(response ='user is not on this project')

    # check issue id is an integer
    try:
        issue_id = int(issue_id)
    except:
        return jsonify(response ='issue ID must be an integer')

    try:
        priority_level = int(priority_level)
    except:
        return False

    # check issue exists
    if cursor.execute("""
        SELECT 1
        FROM issues
        WHERE project_id == ?
            AND issue_id == ?
        ;
        """, [project_id, issue_id]).fetchall is []:
        return jsonify(response ='issue does not exist')

    # function to get date from system
    from datetime import datetime
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # update issue
    cursor.execute("""
        UPDATE issues
        SET title = ?
            , description = ?
            , type_of_issue = ?
            , date_last_updated = ?
            , version_introduced = ?
            , username = ?
            , priority_level = ?
            , status = ?
        WHERE project_id == ?
            AND issue_id == ?
        ;
        """, [title, description, type_of_issue, date, version_introduced, username, priority_level, status, project_id, issue_id])
    db.commit()
