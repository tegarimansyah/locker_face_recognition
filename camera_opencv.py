import cv2
import os
from base_camera import BaseCamera
from pathlib import Path

class Camera(BaseCamera):
    video_source = 0
    save = False

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()
            #print("Img type: ",  type(img))
            if Camera.save:
                if not Path('test.jpg').is_file():
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                    cv2.imwrite("test.jpg", img)
                #print("Save mode: ", Camera.save)
                #yield cv2.imencode('.jpg',cv2.imread('test.jpg'))[1]
                yield cv2.imread('test.jpg')
            else:
                if Path('test.jpg').is_file():
                    os.remove('test.jpg')
                    Camera.name = ""
                # encode as a jpeg image and return it
                yield cv2.imencode('.jpg', img)[1]