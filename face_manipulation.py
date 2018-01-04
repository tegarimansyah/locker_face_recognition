# Command.py
# Aplikasi untuk mengenali wajah manusia
# Oleh: Dwi Fajar Suryanto
#

import command
command.log('Welcome to Face Recognition Software')
command.log('By Dwi Fajar Suranto')

import face_recognition
import cv2
command.log('Program Ready') # +- 28 detik

facedict = {}

def face_init():
    import csv
    import numpy as np
    global facedict
    with open('static/config.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            a = row[2].replace('[','').replace(']','')
            facedict[row[1]] = [float(x) for x in a.rstrip().split()]
    
def encode(filename):
    # menguploud contoh gambardan mempelajari cara mengenalinya .
    image = face_recognition.load_image_file("static/img/"+filename)
    command.log('Image loaded') # +- 0.5 detik
    encoded_image= face_recognition.face_encodings(image)[0]
    command.log('Image encoded')
    face_init()
    return(encoded_image)

def check(img):
    
    # Inisialisasi beberapa vaiable
    face_locations = []
    face_encodings = []
    face_names = []
    name = "Wajah tidak dikenal"
    process_this_frame = True
    global facedict
    
    frame = face_recognition.load_image_file("test.jpg")
    #small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
          
    for face_encoding in face_encodings:
        command.log('Face found, checking')
        match = face_recognition.compare_faces(list(facedict.values()), face_encoding)
        i = 0
        for key, value in facedict.items() :
            if match[i]:
                name = key
                command.log(key + ' detected')
                break
            command.log('Bukan ' + key)
            i+=1
    face_names.append(name)
    
    # menampilkan hasilnya hasilnya
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # mwmbuat skala bingkai untuk wajah
##        top *= 4
##        right *= 4
##        bottom *= 4
##        left *= 4

        # gambar kotak disekitar wajah
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # memberi label dengan nama dibawah wajah
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    
    cv2.imwrite('result.jpg',frame)        
    return (name, cv2.imencode('.jpg',frame)[1].tobytes())
    
    
##
##while True:
##    # mengambil satu bingkai vidio
##    ret, frame = video_capture.read()
##    command.log('Finding face')
##    # ubah ukuran bingkai video menjadi 1/4
##    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
##
##    # proses setiap setiap frame
##    if process_this_frame:
##        # cari semua wajah and dan kodekan wajah pada video
##        face_locations = face_recognition.face_locations(small_frame)
##        face_encodings = face_recognition.face_encodings(small_frame, face_locations)
##
##        face_names = []
##        for face_encoding in face_encodings:
##            # See if the face is a match for the known face(s)
##            command.log('Face found, checking')
##            match = face_recognition.compare_faces([foto1_en, foto2_en, foto3_en], face_encoding)
##            name = "penyusup"
##
##            if match[0]:
##                name = "fajar"
##                command.log('fajar detected')
##                
##            elif match[1]:
##                name = "pakfiqi"
##                command.log('PakFiqi detected')
##            elif match[2]:
##                name = "PakUlum"
##                command.log('PakUlum detected')
##            face_names.append(name)
##
##    process_this_frame = not process_this_frame
##
##
##    # menampilkan hasilnya hasilnya
##    for (top, right, bottom, left), name in zip(face_locations, face_names):
##        # mwmbuat skala bingkai untuk wajah
##        top *= 4
##        right *= 4
##        bottom *= 4
##        left *= 4
##
##        # gambar kotak disekitar wajah
##        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
##
##        # memberi label dengan nama dibawah wajah
##        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
##        font = cv2.FONT_HERSHEY_DUPLEX
##        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
##
##    # menampilkan gambar yg dihasilkan
##    cv2.imshow('Video', frame)
##
##    # push 'q' untuk keluar
##    if cv2.waitKey(1) & 0xFF == ord('q'):
##        break
##
### Release handle to the webcam
##video_capture.release()
##cv2.destroyAllWindows()
