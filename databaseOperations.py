# import sqlite3
import sqlite3

# import get db function to allow the getting of a connection to the database
from database import get_db

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
            return "Username already in use."
            # ('Ewan',) 

    # insert new user into database
    cursor.execute("""
        INSERT INTO users 
        VALUES(?,?)
        ;
        """, [username, password_hash])
    db.commit()

# get all projects that a user is a part of
def get_projects(username, order):
    # initialise connection
    db = get_db()
    cursor = db.cursor()

    # get order column
    if order == "":
        order = "NULL"

    # execute query and return results
    return cursor.execute("""
        SELECT projects.project_id, projects.title, projects.version 
        FROM projects 
        JOIN users_projects_link 
            ON projects.project_id = users_projects_link.project_id
        WHERE username == ?
        ORDER BY ?
        ;
        """, [username, order])

# create new project
def new_project(title, version):
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

# get project info
def get_project_info(project_id, username):
    # initialise connection
    db = get_db()
    cursor = db.cursor()

    # check project id is an integer
    if not isinstance(project_id, int):
        return "Project ID must be an integer."

    # check user is linked to project
    if cursor.execute("""
        SELECT 1
        FROM users_projects_link
        WHERE username == ?
            AND project_id == ?
        ;
        """, [username, project_id]) is None:
        return "User is not on this project."

    # execute query and return results
    return cursor.execute("""
        SELECT * 
        FROM projects
        WHERE project_id == ?
        ;
        """, [project_id])

# get projects users
def get_project_users(project_id, username):
    # initialise connection
    db = get_db()
    cursor = db.cursor()

    # check project id is an integer
    if not isinstance(project_id, int):
        return "Project ID must be an integer."

    # check user is linked to project
    if cursor.execute("""
        SELECT 1
        FROM users_projects_link
        WHERE username == ?
            AND project_id == ?
        ;
        """, [username, project_id]) is None:
        return "User is not on this project."

    # execute query and return results
    return cursor.execute("""
        SELECT username 
        FROM users_projects_link
        WHERE project_id == ?
        ;
        """, [project_id])

# get issues associated with project
def get_project_issues(project_id, order):
    # initialise connection
    db = get_db()
    cursor = db.cursor()

    # check project id is an integer
    if not isinstance(project_id, int):
        return None
    
    # get order column
    if order == "":
        order = "NULL"
    
    # execute query and return results
    return cursor.execute("""
        SELECT *
        FROM issues
        WHERE project_id == ?
        ORDER BY ?
        ;
        """, [project_id, order])

# edit existing project
def edit_project(id, title, version):
    # initalise connection
    db = get_db()
    cursor = db.cursor()

    # check project id is an integer
    if not isinstance(id, int):
        return "Project ID must be an integer."

    # get initial project
    str = ""
    for row in cursor.execute("""
        SELECT *
        FROM projects
        WHERE project_id == ?
        ;
        """, [id]):
        str = row
    
    # create array of new values
    options = [id, title, version]
    # determine replacement project values
    current = str[1:len(str) -2].split(", ")
    new = []
    for option in options:
        if option != "":
            new.append(option)
        else:
            new.append[current[len(new)]]
    
    # delete old project from database
    cursor.execute("""
        DELETE
        FROM projects
        WHERE project_id == ?
        ;
        """, [id])
    db.commit()

    # insert new project into database
    cursor.execute("""
        INSERT INTO projects
        VALUES(?,?,?)
        ;
        """, new)
    db.commit()

# add user to project
def assign_project(username, project_id):
    # initalise connection
    db = get_db()
    cursor = db.cursor()

    # check username is valid
    valid = False
    for row in cursor.execute("""
        SELECT username 
        FROM users
        ;
        """):
        if row[0] == username:
            valid = True
            break
    if not valid:
        return "1"

    # check project id is an integer
    try:
        int(project_id)
    except:
        return "2"

    # check user is not already linked to project
    if cursor.execute("""
        SELECT *
        FROM users_projects_link
        WHERE username == ?
            AND project_id == ?
        ;
        """, [username, project_id]).rowcount() == 0:
        return "3"

    # insert new link between user and project
    cursor.execute("""
        INSERT INTO users_projects_link
        VALUES(?,?)
        ;
        """, [username, project_id])
    db.commit()
    return "4"

# leave project
def leave_project(username, project_id):
    # initalise connection
    db = get_db()
    cursor = db.cursor()

    # check username is valid
    valid = False
    for row in cursor.execute("""
        SELECT username 
        FROM users
        ;
        """):
        if row == username:
            valid = True
            break
    if not valid:
        return None

    # check project id is an integer
    if not isinstance(project_id, int):
        return None

    # check user is linked to project
    if cursor.execute("""
        SELECT 1
        FROM users_projects_link
        WHERE username == ?
            AND project_id == ?
        ;
        """, [username, project_id]) is None:
        return "User is not on this project."

    # remove user from any issues they are assigned on the project
    for row in cursor.execute("""
        SELECT *
        FROM issues
        WHERE username == ? 
            AND project_id == ?
        ;
        """, [username, project_id]):
        new = row[1:len(row) -2].split(", ")
        new[7] = ""
        cursor.execute("""
            INSERT INTO issues
            VALUES(?,?,?,?,?,?,?,?,?,?)
            ;
            """, new)
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
def new_issue(project_id, title, description, type_of_issue, version_introduced, username, priority_level, status):
    # initalise connection
    db = get_db()
    cursor = db.cursor()

    # check project id is an integer
    if not isinstance(project_id, int):
        return "Project ID must be an integer."
    
    # check priority level is empty string or an integer
    if not isinstance(priority_level, int) or priority_level == "":
        return "Priority level must be an empty string or an integer."

    # check project exists
    if cursor.execute("""
        SELECT 1
        FROM projects
        WHERE project_id == ?
        ;
        """, [project_id]) is None:
        return "Project does not exist."
    
    # check user is linked to project
    if cursor.execute("""
        SELECT 1
        FROM users_projects_link
        WHERE username == ?
            AND project_id == ?
        ;
        """, [username, project_id]) is None:
        return "User is not on this project."

    # get next unique issue id value for project
    issue_id = 0
    for row in cursor.execute("""
        SELECT 1 
        FROM issues
        WHERE project_id == ?
        ;
        """[project_id]):
        issue_id += 1
    
    # function to get date from system
    from datetime import datetime
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # insert new issue into database
    cursor.execute("""
        INSERT INTO issues
        VALUES(?,?,?,?,?,?,?,?,?,?)
        ;
        """, [project_id, issue_id, title, description, type_of_issue, date, version_introduced, username, priority_level, status])
    db.commit()

# get issue
def get_issue(project_id, issue_id, username):
    # initalise connection
    db = get_db()
    cursor = db.cursor()

    # check user is linked with project
    if cursor.execute("""
        SELECT 1
        FROM users_projects_link
        WHERE username == ?
            AND project_id == ?
        ;
        """, [username, project_id]) is None:
        return "User is not on this project."    

    # get issue
    return cursor.execute("""
        SELECT *
        FROM issues
        WHERE project_id == ?
            AND issue_id == ?
        ;
        """, [project_id, issue_id])

# edit issue
def edit_issue(project_id, issue_id, title, description, type_of_issue, version_introduced, username, priority_level, status):
    # initalise connection
    db = get_db()
    cursor = db.cursor()

    # check project id is an integer
    if not isinstance(project_id, int):
        return "Project ID must be an integer."
    
    # check user is linked to project
    if cursor.execute("""
        SELECT 1
        FROM users_projects_link
        WHERE username == ?
            AND project_id == ?
        ;
        """, [username, project_id]) is None:
        return "User is not on this project."
    
    # check issue id is an integer
    if not isinstance(issue_id, int):
        return "Issue ID must be an integer."

    # check issue exists
    if cursor.execute("""
        SELECT 1
        FROM issues
        WHERE project_id == ?
            AND issue_id == ?
        ;
        """, [project_id, issue_id]) is None:
        return "Issue does not exist."
    
    # check priority level is empty string or an integer
    if not isinstance(priority_level, int) or priority_level == "":
        return "Priority level must be an empty string or an integer."
    
    # get initial issue
    str = ""
    for row in cursor.execute("""
        SELECT *
        FROM issues
        WHERE project_id == ?
            AND issue_id == ?
        ;
        """, [project_id, issue_id]):
        str = row
    
    # create array of new values
    # function to get date from system
    from datetime import datetime
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    options = [project_id, issue_id, title, description, type_of_issue, date, version_introduced, username, priority_level, status]
    # determine replacement issue values
    current = str[1:len(str) -2].split(", ")
    new = []
    for option in options:
        if option != "":
            new.append(option)
        else:
            new.append[current[len(new)]]
    
    # delete old issue from database
    cursor.execute("""
        DELETE
        FROM issues
        WHERE project_id == ?
            AND issue_id == ?
        ;
        """, [project_id, issue_id])
    db.commit()

    # insert new project into database
    cursor.execute("""
        INSERT INTO issues
        VALUES(?,?,?,?,?,?,?,?,?,?)
        ;
        """, new)
    db.commit()

# delete issue
def delete_issue(project_id, issue_id, username):
    # initalise connection
    db = get_db()
    cursor = db.cursor()

    # check project id is an integer
    if not isinstance(project_id, int):
        return "Project ID must be an integer."
    
    # check user is linked to project
    if cursor.execute("""
        SELECT 1
        FROM users_projects_link
        WHERE username == ?
            AND project_id == ?
        ;
        """, [username, project_id]) is None:
        return "User is not on this project."
    
    # check issue id is an integer
    if not isinstance(issue_id, int):
        return "Issue ID must be an integer."

    # check issue exists
    if cursor.execute("""
        SELECT 1
        FROM issues
        WHERE project_id == ?
            AND issue_id == ?
        ;
        """, [project_id, issue_id]) is None:
        return "Issue does not exist."
    
    # remove issue
    cursor.execute("""
        DELETE FROM issues
        WHERE project_id == ?
            AND issue_id == ?
        ;
        """, [project_id, issue_id])
    db.commit()
