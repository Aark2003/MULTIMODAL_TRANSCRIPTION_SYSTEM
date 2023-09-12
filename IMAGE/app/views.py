from app import app
from flask import render_template, request, redirect, url_for, session
import os
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        session['filename'] = filename
        return redirect(url_for('result'))

@app.route('/result')
def result():
    filename = session['filename']
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    text = pytesseract.image_to_string(Image.open(image_path))
    return render_template('result.html', text=text)
