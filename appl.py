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
    page = []
    page.append('<html><ul>')
    for row in databaseOperations.get_projects("Ewan", ""):
        page.append('<li>')
        page.append(row)
        page.append('</li>')
    page.append('</ul></html>')
    return ''.join(page)

@app.route('/get_project_info')
def getprojectinfo():
    page = []
    page.append('<html><ul>')
    for row in databaseOperations.get_project_info(1, "Ewan"):
        page.append('<li>')
        page.append(str(row[0]))
        page.append(row[1])
        page.append(row[2])
        page.append('</li>')
    page.append('</ul></html>')
    return ''.join(page)

@app.route('/get_project_users')
def getprojectusers():
    page = []
    page.append("<html><ul>")
    for row in databaseOperations.get_project_users(1, "Ewan"):
        page.append("<li>")
        page.append(row)
        page.append("</li>")
    page.append("</ul></html>")
    #return databaseOperations.get_project_users(1, "Ewan")
    return ''.join(page)

@app.route('/assign_project')
def assign():
    return databaseOperations.assign_project("Ewan", 1)
    #return "test"
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
