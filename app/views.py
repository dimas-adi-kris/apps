import os
import json

from app import app
from flask import render_template, request, redirect, jsonify, make_response, send_file, send_from_directory, abort, safe_join, url_for, session
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image
# from app.static.Deployment import predict_bounding_box
# KOMEN DIATAS PENYEBAB ERROR


app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 50 * 1024 * 1024


app.config["SECRET_KEY"] = 'qfLQFMLpUvwRmtBg'


# users = {
# 	"julian": {
# 		"username": "julian",
# 		"email": "julian@gmail.com",
# 		"password": "Xcuy5679-",
# 		"bio": "Some guy from the internet"
# 	},
# 	"clarissa": {
# 		"username": "clarissa",
# 		"email": "clarissa@icloud.com",
# 		"password": "sweetpotato22",
# 		"bio": "Sweet potato is life"
# 	}
# }


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

# @app.route("/profile")
# def profile():

# 	if not session.get("USERNAME") is None:
# 		username = session.get("USERNAME")
# 		user = users[username]
# 		return render_template("public/profile.html", user=user)
# 	else:
# 		print("No username found in session")
# 		return redirect(url_for("sign_in"))


# @app.route('/sign-in', methods = ['GET', 'POST'])
# def sign_in():

# 	if request.method == 'POST':
# 		req = request.form

# 		username = req.get("username")
# 		password = req.get("password")

# 		session.pop('image_name',None)
# 		if not username in users:

# 			print("username not found")
# 			return redirect(request.url)
# 		else:
# 			user = users[username]

# 		if not password == user["password"]:
# 			print("incorrect password")
# 			return redirect(request.url)
# 		else:
# 			session["USERNAME"] = user["username"]

# 			print("session username set")
# 			return redirect(url_for("profile"))
# 	return render_template("public/sign_in.html")
	
# @app.route("/sign-out")
# def sign_out():
# 	session.pop("USERNAME", None)
# 	return redirect(url_for('sign_in'))