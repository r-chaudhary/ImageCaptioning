from flask import Flask
from flask_mysqldb import MySQL
from flask_dropzone import Dropzone
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['UPLOADED_PATH']=os.path.join(basedir, 'uploads')
app.config['ROPZONE_ALLOWED_FILE_TYPE']='image'
app.config['DROPZONE_MAX_FILE_SIZE']=3
app.config['DROPZONE_MAX_FILES']=20
app.config['DROPZONE_UPLOAD_ON_CLICK']=True
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'rahul'
app.config['MYSQL_PASSWORD'] = 'rahul'
app.config['MYSQL_DB'] = 'IMAGE_CAPTION'
app.config['SECRET_KEY'] = 'ecdc7c81f2a175b2f00e89408e73da22'

dropzone = Dropzone(app)
mysql = MySQL(app)

from FlaskApp import routes