from PIL import Image
import face_recognition

image = face_recognition.load_image_file("tes.jpg")

face_locations = face_recognition.face_locations(image)

for face_location in face_locations:

    top, right, bottom, left = face_location

    face_image = image[top-30:bottom+30, left-30:right+30]
    pil_image = Image.fromarray(face_image)
    pil_image.save('search_out.jpg')