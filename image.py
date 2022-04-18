from flask import Flask, flash, request, redirect, url_for , render_template
import urllib.request
import os
from werkzeug.utils import secure_filename

app=Flask(__name__)

ALLOWED_EXTENSION = {'png','jpg','jpeg','gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSION

@app.route('/')
def home():
    return render_template('start.html')

@app.route('/',methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('NO file part')
        return redirect(request.url)
    file= request.files('file')
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename =secure_filename(file_filename)

if __name__ == '__main__':
    app.run(debug=True)