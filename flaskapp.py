import os
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory
import json




input_file_name = 'results.json'
openFile =  open(input_file_name, 'r')
inputFile = json.load(openFile)

subject_wise_results = inputFile['subject_wise_results'] 
student_wise_results = inputFile['student_wise_results']


app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/<path:resource>')
# def serveStaticResource(resource):
#     return send_from_directory('static/', resource)

@app.route("/IT")
def test():
    return "<strong>It's Alive!</strong>"

if __name__ == '__main__':
    app.run()