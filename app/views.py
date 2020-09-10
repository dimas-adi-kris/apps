import os
import json

from app import app
from flask import render_template, request, redirect, jsonify, make_response, send_file, send_from_directory, abort, safe_join, url_for, session
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image
from flask_mysqldb import MySQL
# from app.static.Deployment import predict_bounding_box



app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 50 * 1024 * 1024

app.config["SECRET_KEY"] = 'qfLQFMLpUvwRmtBg'
mysql = MySQL(app)

@app.route("/", methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():

	return render_template("public/index.html")

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
	hists = os.listdir(app.config["IMAGE_UPLOADS"])
	hists = ['/' + file for file in hists]

	if request.method == "POST":

		if request.files:

			image = request.files["image"]

			if image.filename == "":

				feedback = "No filename"
				# print(feedback)

				return render_template("public/upload_image.html",hists=hists, feedback=feedback)

			if allowed_image(image.filename):

				if "filesize" in request.cookies:
					if not allowed_image_filesize(request.cookies["filesize"]):
						print("Filesize exceeded maximum limit")
						return redirect(request.url)

				filename = secure_filename(image.filename)
				session['image_name'] = filename
				# session['image_name_path']
				image.save(os.path.join(app.config["IMAGE_UPLOADS"], session.get('image_name')))

				print("image saved with name", session.get('image_name'))
				
				# simpen ke database
				file = session.get('image_name')
				print('cek1')
				status_detect = "0"
				print('cek1')
				cur = mysql.connection.cursor()
				print('cek1')
				cur.execute("INSERT INTO tb_arrdetect (file,status_detect) VALUES (%s,%s)",(file,status_detect))
				print('cek1')
				mysql.connection.commit()
				print('cek1')

				saved_img = app.config["IMAGE_UPLOADS"] + "/" + session.get('image_name')
				# str_saved_img = str(saved_img)

				# predict_bounding_box.predict(str_saved_img)
				# print(str_saved_img)

				return redirect(request.url)
			
			else:
				print("That file extension is not allowed")
				return redirect(request.url)


	return render_template("public/upload_image.html", hists=hists, saved_image=session.get('image_name'))

@app.route("/arrythmia")
def arrythmia():
	return render_template("public/arrythmia.html")

def allowed_image(filename):
	#kita hanya ingin berkas dengan titik(.) di namanya
	if not "." in filename:
		return False

	#pisahkan ekstensi dari nama berkas
	ext = filename.rsplit(".", 1)[1]
	print(ext)

	#periksa apakah ekstensi-nya ada di ALLOWED_IMAGE_EXTENSIONS
	if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
		return True
	else:
		return False

def allowed_image_filesize(filesize):
	if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
		print(int(filesize))
		return True
	else:
		print(int(filesize))
		return False

@app.route("/table")
def table():
	counter = 0
	counter += 1
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM tb_arrdetect")
	rv = cur.fetchall()
	cur.close()	
	return render_template("public/table.html",computers=rv,counter=counter)

@app.route("/simpan",methods=["GET","POST"])
def simpan():
	file = request.form['file']
	status_detect = request.form['status_detect']
	cur = mysql.connection.cursor()
	cur.execute("INSERT INTO tb_arrdetect (file,status_detect) VALUES (%s,%s)",(file,status_detect))
	mysql.connection.commit()
	return redirect(url_for('table'))

@app.route('/update', methods=["POST"])
def update():
	id_data = request.form['id']
	nama = request.form['nama']
	cur = mysql.connection.cursor()
	cur.execute("UPDATE tb_arrdetect SET file=%s WHERE id=%s", (nama,id_data,))
	mysql.connection.commit()
	return redirect(url_for('table'))

@app.route('/hapus/<string:id_data>', methods=["GET"])
def hapus(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tb_arrdetect WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('table'))