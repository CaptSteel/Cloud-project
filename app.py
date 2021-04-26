import os      # For File Manipulations like get paths, rename
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from PIL import Image
from PIL.ExifTags import TAGS

app = Flask(__name__)  

app.secret_key = "secret key" # for encrypting the session

#It will allow below 1MB contents only
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png','jpeg'])
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
         flash('http://127.0.0.1:5000/metainfo?filename='+filename)
         return redirect('/')
      else:
         flash('Allowed file types are png and jpeg only!')
         return redirect(request.url)
 
@app.route('/metainfo', methods=['GET','POST'])
def metainfo():
   metadict={}
   image_name = request.args.get('filename')
   image_name = "uploads\{}".format(image_name)
   image = Image.open(image_name)# read the image data using PIL
   exifdata = image.getexif() # extract EXIF data
   for tag_id in exifdata:
      # get the tag name, instead of human unreadable tag id
      tag = TAGS.get(tag_id, tag_id)
      data = exifdata.get(tag_id)
      # decode bytes 
      if isinstance(data, bytes):
         data = data.decode()
      if 'DateTimeOriginal' in tag:
         metadict = {"DateTimeOriginal":data}
      if  'OriginalRawFileName' in tag:
         metadict = {"OriginalRawFileName" : data}
   return render_template('metainfo.html',metadict = metadict)
  
if __name__ == '__main__':  
    app.run(debug = True)  