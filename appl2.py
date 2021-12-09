# import python flask library
from flask import Flask, g, redirect, render_template, request, session, url_for

# define app
app = Flask(__name__)

# import database
import db_operations

# login page
@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/submit')
def submit():
    db_operations.new_project((6, "hush", 42))
    return "submit"

@app.route('/edit')
def edit():
    db_operations.edit_project((1, "foo2: electric boogaloo", 2))
    return redirect(url_for('view'))

@app.route('/view')
def get_projects():
    page =[]
    page.append('<html><ul>')
    for row in db_operations.get_project_info([1]):
        page.append('<li>')
        page.append(row)
        page.append('</li>')
    page.append('</ul></html>')
    return ''.join(page)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

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
    for row in db_operations.get_project_users(1, "Ewan").json['records']:
        page.append("<li>")
        page.append(''.join(row))
        page.append("</li>")
    page.append("</ul></html>")
    return ''.join(page)

@app.route('/assign_project')
def assign():
    return db_operations.assign_project("Ewan", 1).json['response']
    # return "test"
    