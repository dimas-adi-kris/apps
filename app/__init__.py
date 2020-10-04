
from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)



from app import views
from app import sublink

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")
print(f'ENV is set to: {app.config["ENV"]}')