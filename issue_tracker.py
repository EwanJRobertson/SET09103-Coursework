# import python flask library
from flask import Flask, g, redirect, render_template, request, session, url_for
import json

# define app
app = Flask(__name__)

# import database
import db_operations

# login page
@app.route('/')
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        return "Post"
    else:
        return "Get"

@app.route('/new_user')
def newuser():
    db_operations.new_user("Ewan", "password")
    return "test"

@app.route('/new_project')
def newproject():
    db_operations.new_project("foo", "version")
    return "test"

@app.route('/get_projects')
def getprojects():
    page = []
    page.append('<html><ul>')
    for row in db_operations.get_projects("Ewan", ""):
        page.append('<li>')
        page.append(row)
        page.append('</li>')
    page.append('</ul></html>')
    return ''.join(page)

@app.route('/get_project_info')
def getprojectinfo():
    page = []
    page.append('<html><ul>')
    for row in db_operations.get_project_info(1, "Ewan"):
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
    #for row in db_operations.get_project_users(1, "Ewan").json['records']:
    #    page.append("<li>")
    #    page.append(row)
    #    page.append("</li>")
    page.append("<li>")
    page.append(''.join(db_operations.get_project_users(1, "Ewan").json['records']))
    page.append("</li>")
    page.append("</ul></html>")
    return ''.join(page)

@app.route('/assign_project')
def assign():
    return db_operations.assign_project("Ewan", 1).json['response']
    # return "test"
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
