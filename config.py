class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    DEBUG = True

    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'db_apps'


    IMAGE_UPLOADS = "./app/static/Deployment/Predicting/"
    ALLOWED_IMAGE_EXTENSIONS = ["JPEG", "JPG", "PNG", "GIF"]

    ALLOWED_XML_EXTENSIONS = ["XML"]

    XML_UP = "./app/static/AF"

    SESSION_COOKIE_SECURE = False

class DevelopmentConfig(Config):
    DEBUG = True

    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    IMAGE_UPLOADS = "./app/static/Deployment/Predicting/"

    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = False
