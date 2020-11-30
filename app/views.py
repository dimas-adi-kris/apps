import os
import json

from app import app
from flask import render_template, request, redirect, jsonify, make_response, send_file, send_from_directory, abort, safe_join, url_for, session
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image
from flask_mysqldb import MySQL
# from app.static.Deployment import predict_bounding_box


from app.static.AF import inference

from MySQLdb import _exceptions



# app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 50 * 1024 * 1024

app.config["SECRET_KEY"] = 'qfLQFMLpUvwRmtBg'
mysql = MySQL(app)

@app.route("/", methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
	session.clear()
	return render_template("public/index.html")

@app.route("/tableAF")
def tableAF():
	session.clear()
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM tb_af")
	rv = cur.fetchall()

	cur.close()	
	return render_template("public/table.html",computers=rv)

@app.route("/getTabel", methods=["GET","POST"])
def getTabel():
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM tb_af")

	row_headers=[x[0] for x in cur.description] #this will extract row headers

	rv = cur.fetchall()

	cur.close()	
	json_data=[]
	for result in rv:
		json_data.append(dict(zip(row_headers,result)))
	return jsonify(json_data)


# @app.route("/saved_image",methods=["GET"])
# def saved_image():
# 	cur = mysql.connection.cursor()
# 	cur.execute("select * from tb_arrdetect")
# 	rv = cur.fetchall()
# 	cur.close()
# 	return render_template('public/recorded_image.html',computers=rv)

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
	status_detect = request.form['status_detect']
	cur = mysql.connection.cursor()
	cur.execute("UPDATE tb_arrdetect SET file=%s,status_detect=%s WHERE id_detect=%s", (nama,status_detect,id_data))
	mysql.connection.commit()
	return redirect(url_for('table'))

@app.route('/hapus/<string:id>', methods=["GET"])
def hapus(id):
	cur = mysql.connection.cursor()
	cur.execute("DELETE FROM tb_arrdetect WHERE id_detect=%s", (id,))
	cur.execute("update tb_arrdetect set id_detect=id_detect-1 where id_detect > %s",(id,))
	cur.execute("ALTER TABLE tb_arrdetect AUTO_INCREMENT=1;")
	mysql.connection.commit()
	return redirect(url_for('table'))

@app.route('/detail/<string:ids>')
def detail(ids):
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM tb_af WHERE id=%s", (ids,))
	rv = cur.fetchall()
	print(rv)

	cur.close()	
	return render_template("public/detail.html",computers=rv)

@app.route("/Atrial", methods=["GET","POST"])
def atrial():
	
	if request.method == "POST":
		xml = request.files["xml"]
		if xml.filename == "":
			feedback = "No filename"
			return render_template("public/Atrial.html",feedback=feedback)

		if allowed_xml(xml.filename):
			filename = secure_filename(xml.filename)
			session['xml_name'] = filename
			xml.save(os.path.join(app.config["XML_UP"], session.get('xml_name')))
			saved_xml = str(app.config["XML_UP"]+"/"+session.get('xml_name'))
			print(saved_xml)
			hasil,file = inference.utama(saved_xml)
			session['hasil'] = hasil
			session['file'] = file
			print("hasil tes nya adalah ",hasil)
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO tb_AF (file,status_detect) VALUES (%s,%s)",(file,hasil))
			mysql.connection.commit()

			return redirect(request.url)

	return render_template("/public/atrial.html",hasil=session.get('hasil'),nama_file=session.get('file'))

@app.route('/getDataByID',methods=["GET","POST"])
def get():
	# if request.method == "POST":
	data_id = request.form['data_id']
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM tb_af WHERE id=%s", (data_id))
	row_headers=[x[0] for x in cur.description] #this will extract row headers

	rv = cur.fetchall()
	cur.close

	json_data=[]
	for result in rv:
		json_data.append(dict(zip(row_headers,result)))
	return jsonify(json_data[0])

# @app.route("/upload-image", methods=["GET", "POST"])
# def upload_image():

# 	if request.method == "POST":
# 		if request.files:
# 			image = request.files["image"]
# 			if image.filename == "":
# 				feedback = "No filename"
# 				# print(feedback)
# 				return render_template("public/upload_image.html", feedback=feedback)

# 			if allowed_image(image.filename):
# 				if "filesize" in request.cookies:
# 					if not allowed_image_filesize(request.cookies["filesize"]):
# 						print("Filesize exceeded maximum limit")
# 						return redirect(request.url)

# 				filename = secure_filename(image.filename)
# 				session['image_name'] = filename
# 				# session['image_name_path']
# 				image.save(os.path.join(app.config["IMAGE_UPLOADS"], session.get('image_name')))
# 				print("image saved with name", session.get('image_name'))
# 				saved_img = app.config["IMAGE_UPLOADS"] + "/" + session.get('image_name')
# 				str_saved_img = str(saved_img)
# 				print(str_saved_img)
# 				predict_bounding_box.predict(str_saved_img)
# 				# print(str_saved_img)
# 				# simpen ke database
# 				file = session.get('image_name')
# 				status_detect = "0"
# 				cur = mysql.connection.cursor()
# 				cur.execute("INSERT INTO tb_arrdetect (file,status_detect) VALUES (%s,%s)",(file,status_detect))
# 				mysql.connection.commit()
# 				return redirect(request.url)
			
# 			else:
# 				print("That file extension is not allowed")
# 				return redirect(request.url)
# 	return render_template("public/upload_image.html", saved_image=session.get('image_name'))

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

def allowed_xml(filename):
	#kita hanya ingin berkas dengan titik(.) di namanya
	if not "." in filename:
		return False

	#pisahkan ekstensi dari nama berkas
	ext = filename.rsplit(".", 1)[1]
	print(ext)

	#periksa apakah ekstensi-nya ada di ALLOWED_IMAGE_EXTENSIONS
	if ext.upper() in app.config["ALLOWED_XML_EXTENSIONS"]:
		return True
	else:
		return False

@app.route("/table")
def table():
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM tb_arrdetect")
	rv = cur.fetchall()

	cur.close()	

	return render_template("public/table.html",computers=rv)

