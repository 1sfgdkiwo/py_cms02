from flask import Flask

import os
import os.path as op

# from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'r4sy4_ub4y'
# app.config['DATABASE_FILE'] = 'cms01'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:r3j3k1ul0@postgres/' + app.config['DATABASE_FILE']

# rumus
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://username:password@localhost:5432/dbname'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:r3j3k1ul0@localhost/cms01'

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SECURITY_PASSWORD_SALT'] = 'r3j3k1ulo'





#development, set 0 to refresh static cache
# SEND_FILE_MAX_AGE_DEFAULT = 0

# Create directory for file fields to use
FILE_PATH = op.join(op.dirname(__file__), 'static', 'upload')
try:
    os.mkdir(FILE_PATH)
except OSError:
    pass

ALLOWED_EXTENSIONS = set(['bmp', 'png', 'jpg', 'jpeg', 'gif'])