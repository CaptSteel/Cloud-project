import os      # For File Manipulations like get paths, rename
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from PIL import Image
from PIL.ExifTags import TAGS

app = Flask(__name__)  

app.secret_key = "secret key" # for encrypting the session
mylist = []

#It will allow below 1MB contents only
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'static\\uploads\\')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png','jpeg', 'jpg'])
def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')  
def upload():  
   return render_template("index.html")  
 
@app.route('/', methods=['POST'])
def upload_file(): 
   if request.method == 'POST':
      # check if the post request has the file part
      if 'file' not in request.files:
         flash('No file part')
         return redirect(request.url)
      file = request.files['file']
      if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
      if file and allowed_file(file.filename):
         filename = secure_filename(file.filename)
         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
         flash('http://127.0.0.1:5000/metainfo/'+filename)
         mylist.append('http://127.0.0.1:5000/metainfo/'+filename)
         return redirect('/')
      else:
         flash('Allowed file types are png and jpeg only!')
         return redirect(request.url)
 
@app.route('/metainfo/<filename>', methods=['GET','POST'])
def metainfo(filename):
   metadict={}
   image_name = UPLOAD_FOLDER + filename
   filedir = 'uploads\\'+ filename
   image = Image.open(image_name)# read the image data using PIL
   exifdata = image.getexif() # extract EXIF data
   for tag, value in exifdata.items():
      decoded = TAGS.get(tag, tag)
      metadict[decoded] = value
   return render_template('metainfo.html', metadict = metadict, image_name = image_name, filedir = filedir)

@app.route('/mylinks', methods=['GET','POST'])
def mylinks():
   return render_template('mylinks.html', mylist = mylist)


if __name__ == '__main__':  
    app.run(debug = True)  