# import python flask library
from flask import Flask, g, redirect, render_template, request, session, url_for

# define app
app = Flask(__name__)

# import database
import databaseOperations

# login page
@app.route('/')
@app.route('/test')
def test():
    return "test"

@app.route('/new_user')
def newuser():
    databaseOperations.new_user("Ewan", "password")
    return "test"

@app.route('/new_project')
def newproject():
    databaseOperations.new_project("foo", "version")
    return "test"

@app.route('/get_projects')
def getprojects():
    for row in databaseOperations.get_projects("Ewan", ""):
        print(row)

@app.route('/get_project_info')
def getprojectinfo():
    for row in databaseOperations.get_project_info(1, "Ewan"):
        print(row)

@app.route('/get_project_users')
def getprojectusers():
    for row in databaseOperations.get_project_users(1, "Ewan"):
        print(row)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)