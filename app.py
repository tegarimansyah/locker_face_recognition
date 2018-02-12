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
checking_done = False

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    label=''
    if request.method == 'POST':
        global checking_done
        global name
        if request.form['submit'] == 'Buka Loker':
            Camera.save = not Camera.save
            if Camera.save:
                from time import sleep
                print('Memeriksa Wajah')

                checking_done = False
                while not checking_done:
                    pass
                
                if not name is "Wajah tidak dikenal":
                    print('Membuka loker milik: ' + name)
                    label = 'Membuka Loker Milik ' + name
                    
                    import serial
                    ser = serial.Serial("/dev/serial0",9600)
                    ser.write(name)
                    
                else:
                    print('Wajah tidak dikenal')
                    label = 'Wajah tidak dikenal'
            else:
                checking_done = False
                print('Menunggu perintah')
                label = ''
                
    return render_template('index.html', label=label)

def gen(camera):
    while True:
        if camera.save:
             import cv2
             img = camera.get_frame()
             global name
             global checking_done
             if not checking_done:
                 name, frame = check(img)
                 checking_done = True
                 print("Checking Done")
             frame = cv2.imencode('.jpg',cv2.imread('result.jpg'))[1].tobytes()
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
        try:
            if request.form['hapus'] == 'Hapus':
                print('menghapus ' + request.form['nama'])
                # mungkin ada yang harus di close
                reader = csv.reader(open('static/config.csv'), delimiter=',')
                f = csv.writer(open("static/config.backup.csv", "w"))
                for line in reader:
                    if request.form['nama'] not in line:
                        f.writerow(line)
                os.rename('static/config.backup.csv','static/config.csv')
                return redirect(url_for('pengaturan'))
        except:
            pass
        
        try:
            if request.form['edit'] == 'Edit':
                print('mengedit ' + request.form['nama'])
                return redirect(url_for('pengaturan'))
        except:
            pass
        
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
                print(data)
                a.writerows(data) 
    face_init()
    
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