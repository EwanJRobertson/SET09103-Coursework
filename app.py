# import python flask library
from flask import Flask, redirect, render_template, request, session, url_for

from flask import Flask

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