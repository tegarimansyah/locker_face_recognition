from PIL import Image, ImageDraw
import face_recognition

image = face_recognition.load_image_file("search_out.jpg")

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
    
    pil_image.save('facial_out.jpg')