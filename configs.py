   
import os 

class Config(object):
    SECRET_KEY = os.urandom(32)
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres@alusocial:123456Ahmed@alusocial.postgres.database.azure.com:5432/"  + 'alu_social?sslmode=require'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True
    


