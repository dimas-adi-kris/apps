from app import app
from flask import render_template, request, redirect, jsonify, make_response, send_file, send_from_directory, abort, safe_join, url_for, session
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL

@app.route('/kakryan')
def kakryan():
    return render_template('public/kakryan.html')

@app.route('/atrial_fibrilation', methods=["POST"])
def atrial_fibrilation():
    if request.method == "POST":
        if request.files:
            file_diterima = request.files['atr']
            if file_diterima.filename == "":
                feedback = "No filename"
                return render_template('public/atrial_fibrilation', feedback=feedback)
            
            filename = secure_filename(file_diterima.filename)
            session['file_diterima'] = filename

            file_diterima.save(os.path.join(app.config['IMAGE_UPLOADS'], session.get('file_diterima')))

            saved_file = app.config["IMAGE_UPLOADS"] + "/" + session.get('file_diterima')
    return render_template('public/atrial_fibrilation')