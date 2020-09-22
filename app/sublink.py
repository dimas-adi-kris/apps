from app import app
from flask import render_template, request, redirect, jsonify, make_response, send_file, send_from_directory, abort, safe_join, url_for, session
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL

@app.route('/kakryan')
def kakryan():
    return render_template('public/kakryan.html')

