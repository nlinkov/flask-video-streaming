
import cv2
from base_camera import BaseCamera

import numpy as np
from datetime import datetime

def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)

threshold = 68000

class Camera(BaseCamera):
    video_source = 0

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        t_minus = cv2.cvtColor(camera.read()[1], cv2.COLOR_RGB2GRAY)
        t = cv2.cvtColor(camera.read()[1], cv2.COLOR_RGB2GRAY)
        t_plus = cv2.cvtColor(camera.read()[1], cv2.COLOR_RGB2GRAY)
        timeCheck = datetime.now().strftime('%Ss')

        while True:
            # read current frame
            _, frame = camera.read()          # read from camera
            totalDiff = cv2.countNonZero(diffImg(t_minus, t, t_plus))  # this is total difference number
            text = "threshold: " + str(totalDiff)      # make a text showing total diff.
            cv2.putText(frame, text, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)   # display it on screen
            if totalDiff > threshold and timeCheck != datetime.now().strftime('%Ss'):
               dimg = camera.read()[1]
               cv2.imwrite('data/' + datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + '.jpg', dimg)
            timeCheck = datetime.now().strftime('%Ss')
            # Read next image
            t_minus = t
            t = t_plus
            t_plus = cv2.cvtColor(camera.read()[1], cv2.COLOR_RGB2GRAY)

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', frame)[1].tobytes()
