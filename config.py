import os

"""
geting secret key which reduce risk form hacking!
"""
SECRET_KEY = os.urandom(32)

"""
debug mode
"""
DEBUG = True

"""
sqlalchemy configs
"""
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
