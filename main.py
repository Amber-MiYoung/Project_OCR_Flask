#app.py
import subprocess
from charset_normalizer import detect
from flask import Flask, flash, request, redirect, url_for, render_template, send_file
import urllib.request
import os
#import sys
from surprise import Prediction
from werkzeug.utils import secure_filename
from utils.general import methods


 
#TEMPLATE_DIR = os.path.abspath('../templates')
#STATIC_DIR = os.path.abspath('../static')
app = Flask(__name__, template_folder='templates')


 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        #subprocess.run("ls")
        subprocess.run(['python', 'detect.py', '--source', os.path.join(app.config['UPLOAD_FOLDER'], filename),'--weight','best.pt','--img','416','--save-txt','--save-conf'])
        

        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>', methods=['GET'])
def display_image(filename):
    #print('display_image filename: ' + filename)
    #obj = request.args.get('obj')
        #rint(obj)
    #loc = os.path.join("runs/detect/exp", obj) 
    #print(loc)
    #try:
    #    return render_template('index.html', filename=send_file(os.path.join("runs/detect/exp", obj)))
    #except Exception as e:
    #   return str(e)


    return redirect(url_for('static', filename='runs/detect/exp/' + filename), code=301)


#@app.route('/prediction', methods=['POST'])
##def predict(filename):
 #   if request.method=="POST":
#        return
##    file = redirect(url_for('static', filename='uploads/' + filename), code=301)
 #   return file
    #filename = secure_filename(file.filename)
    #subprocess.run("ls")
    #subprocess.run(['python3', 'detect.py', '--source', os.path.join('uploads',filename),'--weight','best.pt','--img','416','--save','-txt','--save','-conf'])
    #obj = secure_filename(file.filename)
    #return  obj
    #return render_template('index.html')
 
if __name__ == "__main__":
    app.run()
