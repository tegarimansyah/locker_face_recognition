from flask import Flask, jsonify, render_template, Response
import os
# import numpy as np
import cv2
from PIL import Image, ImageDraw
import face_recognition
import serial


app = Flask(__name__, static_folder='static')

def ambil_gambar():
    cap = cv2.VideoCapture(0)
    _,frame = cap.read()
    cv2.imwrite(test_data_url,frame)
    cap.release()

def compare(photo_id):

    known_image = face_recognition.load_image_file('static/image/' + images[photo_id-1])
    image = face_recognition.load_image_file(test_data_url)

    biden_encoding = face_recognition.face_encodings(known_image)[0]

    try:
        unknown_encoding = face_recognition.face_encodings(image)[0]
        encoding[0], encoding[1] = biden_encoding, unknown_encoding
    except:
        print('Tidak ada wajah')
        encoding[0], encoding[1] = '', 'Tidak Ditemukan Wajah'
        return False
    

    face_landmarks_list = face_recognition.face_landmarks(image)

    for face_landmarks in face_landmarks_list:
        pil_image = Image.fromarray(image)
        d = ImageDraw.Draw(pil_image, 'RGBA')

        d.line(face_landmarks['left_eyebrow'], fill=(255, 255, 255, 255), width=2)
        d.line(face_landmarks['right_eyebrow'], fill=(255, 255, 255, 255), width=2)

        d.line(face_landmarks['top_lip'], fill=(255, 255, 255, 255), width=2)
        d.line(face_landmarks['bottom_lip'], fill=(255, 255, 255, 255), width=2)

        d.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=(255, 255, 255, 255), width=2)
        d.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=(255, 255, 255, 255), width=2)

        d.line(face_landmarks['chin'], fill=(255, 255, 255, 255), width=2)
        d.line(face_landmarks['nose_bridge'], fill=(255, 255, 255, 255), width=2)
        
        pil_image.save(test_data_url)
    
    result = face_recognition.compare_faces([biden_encoding], unknown_encoding)[0]
    
    return result


def cek_wajah(photo_id):
    ambil_gambar()
    result = compare(photo_id)

    if result:
        if serial_available:
            kirim_data = photo_id
            ser.write(kirim_data.encode())
        else:
            print('Serial not available')
        return True
    return False

@app.after_request
def apply_caching(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate" # HTTP 1.1.
    response.headers["Pragma"] = "no-cache" # HTTP 1.0.
    response.headers["Expires"] = "0" # Proxies.
    return response


@app.route('/')
def root():
    return render_template('index.html', data=data)

@app.route('/cek/<int:photo_id>')
def mengenali_wajah(photo_id):
    success = cek_wajah(photo_id)
    return render_template('cek.html', data=data[photo_id-1], success=success, test_face_url='http://localhost:5000/'+test_data_url, encoding=encoding)

if __name__ == '__main__':
    try:
        ser = serial.Serial("/dev/serial0",9600)
        serial_available = True
    except:
        print('Serial not available')
        serial_available = False
        
    encoding = [0, 0]
    images = sorted(os.listdir('static/image/'))
    data = []
    for image in images:
        new_data = {}
        new_data['url'] = 'http://localhost:5000/static/image/' + image.replace(' ','%20')
        new_data['id'], new_data['name'], _ = image.split('.')
        data.append(new_data)

    test_data_url = 'static/test.jpg'

    app.run(debug=True)