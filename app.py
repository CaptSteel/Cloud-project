from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'jpeg','png'}
def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
app.secret_key = b'secret'
@app.route('/', methods=['GET', 'POST'])
def index():
   if request.method == 'POST':
       

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'

