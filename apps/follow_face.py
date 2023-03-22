# OpenCV program to detect face in real time
# import libraries of python OpenCV
# where its functionality resides

from lib.irobot_lib.iRobot import iRobot
from threading import Thread
import cv2
import time
import numpy as np

# load the required trained XML classifiers
# https://github.com/Itseez/opencv/blob/master/
# data/haarcascades/haarcascade_frontalface_default.xml
# Trained XML classifiers describes some features of some
# object we want to detect a cascade function is trained
# from a lot of positive(faces) and negative(non-faces)
# images.
# face_cascade = cv2.CascadeClassifier(
#   'lib/haarcascade/haarcascade_frontalface_default.xml')


class ThreadedCamera(object):
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # FPS = 1/X
        # X = desired FPS
        self.FPS = 1/25
        self.FPS_MS = int(self.FPS * 1000)

        # Start frame retrieval thread
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

        # Variables
        self.deadZone = 200

        self.rotateCommand = None
        self.moveCommand = None

    def update(self):
        while True:
            if self.cap.isOpened():
                (self.status, self.frame) = self.cap.read()

                # convert to gray scale of each frames
                gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

                # Detects faces of different sizes in the input image
                self.faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

                height, width, rgb = np.shape(self.frame)

                for (x, y, w, h) in self.faces:
                    leftBoundary = x+w/2+self.deadZone/2
                    rightBoundary = x+w/2-self.deadZone/2

                    cv2.rectangle(self.frame, (x, y),
                                  (x+w, y+h), (255, 255, 0), 2)

                    if(leftBoundary < width/2):
                        print("go right")
                        self.rotateCommand = "Right"
                    elif(rightBoundary > width/2):
                        print("go left")
                        self.rotateCommand = "Left"
                    else:
                        # print("stop")
                        # self.rotateCommand = "Stop"
                        if(w < width/5):
                            print("Fwd")
                            self.moveCommand = "Fwd"
                        if(w > width/3):
                            print("Bwd")
                            self.moveCommand = "Bwd"
                        else:
                            print("Stop")
                            self.moveCommand = "Stop"

            time.sleep(self.FPS)

    def show_frame(self):
        cv2.imshow('frame', self.frame)
        cv2.waitKey(self.FPS_MS)

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    src = 0
    threaded_camera = ThreadedCamera(src)

    # create irobot instance
    robot = iRobot()

    while True:
        try:
            threaded_camera.show_frame()
        except AttributeError:
            pass

        if(threaded_camera.rotateCommand == "Right"):
            robot.turnRight(speed=0.03)
        elif(threaded_camera.rotateCommand == "Left"):
            robot.turnLeft(speed=0.03)
        elif(threaded_camera.rotateCommand == "Stop"):
            robot.turnRight(speed=0.0)  # Stop command not working.
            # robot.moveStop()
        elif(threaded_camera.moveCommand == "Fwd"):
            robot.moveForward(speed=0.1)
        elif(threaded_camera.moveCommand == "Bwd"):
            robot.moveBackwards(speed=0.1)
        elif(threaded_camera.moveCommand == "Stop"):
            robot.moveForward(speed=0.0)  # Stop command not working.
            # robot.moveStop()

        # Wait for Esc key to stop
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
