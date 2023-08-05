from wsgiref.simple_server import make_server
from flask import Flask, request, jsonify, render_template, flash, session, redirect, url_for, Blueprint
import json
from database.db_service import *
import os
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'app'  # Replace 'your_secret_key_here' with a unique and secure string
CORS(app)  # Add this line to enable CORS support for the entire app

msg = ""

# Home route
@app.route('/')
def home():
    if not ('logged_in' in session and session['logged_in']):
        return redirect(url_for('login'))

    return redirect("/loan_applications")

# The rest of the app routes and functions go here...


def application(environ, start_response):
    # Using the provided WSGI server, call the Flask app to handle the request
    app_response = app(environ, start_response)

    # Return the app response as the WSGI application response
    return app_response


if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'static/uploads'

    # Create a WSGI server and run the Flask app using the WSGI application
    server = make_server('localhost', 5000, application)
    print("WSGI Server started on http://localhost:5000")
    server.serve_forever()
