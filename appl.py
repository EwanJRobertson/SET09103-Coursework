# import python flask library
from flask import Flask, g, redirect, render_template, request, session, url_for
from appl2 import get_projects

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

@app.route('/new_project')
def newproject():
    databaseOperations.new_project("foo", "version")

@app.route('/get_projects')
def getprojects():
    databaseOperations.get_projects("Ewan", "")

@app.route('/get_project_info')
def getprojectinfo():
    databaseOperations.get_project_info(1, "Ewan")

@app.route('/get_project_users')
def getprojectusers():
    databaseOperations.get_project_users(1, "Ewan")
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)