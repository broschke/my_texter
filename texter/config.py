import os

# class DevelopmentConfig(object):
#     SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/texter"
#     DEBUG = True
#     SECRET_KEY = os.environ.get("TEXTER_SECRET_KEY", os.urandom(12))
   

class ProductionConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    DEBUG = True
    SECRET_KEY = os.environ.get("TEXTER_SECRET_KEY", os.urandom(12))
