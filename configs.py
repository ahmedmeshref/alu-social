   
import os 

class Config(object):
    SECRET_KEY = os.urandom(32)
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("POSTGRESQL") + 'alu_social'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True
    
