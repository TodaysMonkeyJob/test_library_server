import os

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(basedir, 'app.db')

MAX_CONTENT_LENGTH = 1024 * 1024

UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'upload/')

# TODO: change to env vars
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:353535@localhost:5405/library"

SECRET_KEY = 'you-will-never-guess'

FLASKY_ADMIN = 'root@gmail.com'

SQLALCHEMY_TRACK_MODIFICATIONS = False