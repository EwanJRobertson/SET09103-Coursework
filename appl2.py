# import python flask library
from flask import Flask, g, redirect, render_template, request, session, url_for

# define app
app = Flask(__name__)

# import database
import database
import databaseOperations

# login page
@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/submit')
def submit():
    return "submit"

@app.route('/view')
def view():
    page =[]
    page.append('<html><ul>')
    for row in databaseOperations.get_project_info(database.get_db(),1):
        page.append('<li>')
        page.append(str(row))
        page.append('</li>')
    page.append('</ul></html>')
    return ''.join(page)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)