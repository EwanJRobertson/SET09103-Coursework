# import python flask library
from flask import Flask, g, redirect, render_template, request, session, url_for

# define app
app = Flask(__name__)

# import database
import databaseOperations

# login page
@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/submit')
def submit():
    databaseOperations.new_project((6, "hush", 42))
    return "submit"

@app.route('/edit')
def edit():
    databaseOperations.edit_project((1, "foo2: electric boogaloo", 2))
    return redirect(url_for('view'))

@app.route('/view')
def get_projects():
    page =[]
    page.append('<html><ul>')
    for row in databaseOperations.get_project_info([1]):
        page.append('<li>')
        page.append(row)
        page.append('</li>')
    page.append('</ul></html>')
    return ''.join(page)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
