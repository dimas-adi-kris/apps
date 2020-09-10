class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    DEBUG = True

    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    IMAGE_UPLOADS = "C:/app/app/static/Deployment/Predicting/"

    SESSION_COOKIE_SECURE = False

class DevelopmentConfig(Config):
    DEBUG = True

    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    IMAGE_UPLOADS = "/home/isysrg/app/app/app/static/Deployment/Predicting/"

    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = False
