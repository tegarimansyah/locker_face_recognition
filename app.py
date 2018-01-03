#!/usr/bin/env python
from importlib import import_module
import os
import csv
from flask import Flask, render_template, Response, request, send_from_directory, redirect, url_for
from werkzeug import secure_filename
from face_manipulation import encode, check, face_init

Camera = import_module('camera_opencv').Camera
UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
name = ''

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    label=''
    if request.method == 'POST':
        if request.form['submit'] == 'Buka Loker':
            Camera.save = not Camera.save
            if Camera.save:
##                import time
##                time.sleep(3)
                global name
                if name is not "Tidak ditemukan":
                    label = 'Membuka Loker Milik ' + name
                else:
                    label = 'Wajah tidak dikenal'
            else:
                label = ''
                
    return render_template('index.html', label=label)

def gen(camera):
    while True:
        if camera.save:
             img = camera.get_frame()
             global name
             name, frame = check(img)
        else:
             frame = camera.get_frame().tobytes()
             
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/pengaturan', methods=['GET', 'POST'])
def pengaturan():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            from pathlib import Path
            check = Path('static/img/'+filename)
            while not check.is_file():
                pass # Menunggu selesai upload
            
            encoded = encode(filename)
            with open('static/config.csv', 'a') as fp:
                a = csv.writer(fp, delimiter=',')
                data = [[filename, request.form['nama'], encoded]]
                a.writerows(data)
            return redirect(url_for('pengaturan'))
    
    with open('static/config.csv') as f:
        reader = csv.reader(f)
        return render_template('pengaturan.html', reader=reader)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
if __name__ == '__main__':
    face_init()
    app.run(host='0.0.0.0', threaded=True)
