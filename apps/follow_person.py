# OpenCV program to detect face in real time
# import libraries of python OpenCV
# where its functionality resides

from lib.irobot_lib.iRobot import iRobot
from threading import Thread
import cv2
import time
import numpy as np
from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import argparse


# load the required trained XML classifiers
# https://github.com/Itseez/opencv/blob/master/
# data/haarcascades/haarcascade_frontalface_default.xml
# Trained XML classifiers describes some features of some
# object we want to detect a cascade function is trained
# from a lot of positive(faces) and negative(non-faces)
# images.
# face_cascade = cv2.CascadeClassifier(
#   'lib/haarcascade/haarcascade_frontalface_default.xml')


class YOLO(object):
    def __init__(self, src=0):
        self.path = "apps/lib/mobileNetSSD/"
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                        "sofa", "train", "tvmonitor"]
        self.COLORS = np.random.uniform(0, 255, size=(len(self.CLASSES), 3))

        # load our serialized model from disk
        print("[INFO] loading model...")
        self.net = cv2.dnn.readNetFromCaffe(
            self.path+'MobileNetSSD_deploy.prototxt.txt', self.path+'MobileNetSSD_deploy.caffemodel')

        # initialize the video stream, allow the cammera sensor to warmup,
        # and initialize the FPS counter
        print("[INFO] starting video stream...")
        self.vs = VideoStream(src=0).start()
        time.sleep(2.0)
        self.fps = FPS().start()

        # # Start self.frame retrieval thread
        # self.thread = Thread(target=self.update, args=())
        # self.thread.daemon = True
        # self.thread.start()

        # FPS = 1/X
        # X = desired FPS
        self.FPS = 1/25
        self.FPS_MS = int(self.FPS * 1000)

        # Variables
        self.deadZone = 200

        self.rotateCommand = None
        self.moveCommand = None

    def update(self):
        print("update")
        while True:
            print("new frame")
            self.frame = self.vs.read()
            self.frame = imutils.resize(self.frame, width=400)

            # grab the self.frame dimensions and convert it to a blob
            (h, w) = self.frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(self.frame, (300, 300)),
                                         0.007843, (300, 300), 127.5)

            # pass the blob through the network and obtain the detections and
            # predictions
            self.net.setInput(blob)
            detections = self.net.forward()

            # loop over the detections
            for i in np.arange(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with
                # the prediction
                confidence = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence
                if confidence > 0.2:
                    # extract the index of the class label from the
                    # `detections`, then compute the (x, y)-coordinates of
                    # the bounding box for the object
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    # draw the prediction on the self.frame
                    label = "{}: {:.2f}%".format(self.CLASSES[idx],
                                                 confidence * 100)
                    cv2.rectangle(self.frame, (startX, startY), (endX, endY),
                                  self.COLORS[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(self.frame, label, (startX, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.COLORS[idx], 2)
                    if self.CLASSES[idx] == "person":
                        print("detected person")
                        print(i)
                        # follow commands
                        mx = startX + (endX-startX)/2.0
                        my = startY + (endY-startY)/2.0
                        wi = (endX-startX)
                        he = (endY-startY)
                        print(startX)
                        print(startY)
                        break
                        # for (x, y, w, h) in self.faces:
                        #     leftBoundary = x+w/2+self.deadZone/2
                        #     rightBoundary = x+w/2-self.deadZone/2

                        #     cv2.rectangle(self.self.frame, (x, y),
                        #                   (x+w, y+h), (255, 255, 0), 2)

                        #     if(leftBoundary < width/2):
                        #         print("go right")
                        #         self.rotateCommand = "Right"
                        #     elif(rightBoundary > width/2):
                        #         print("go left")
                        #         self.rotateCommand = "Left"
                        #     else:
                        #         # print("stop")
                        #         # self.rotateCommand = "Stop"
                        #         if(w < width/5):
                        #             print("Fwd")
                        #             self.moveCommand = "Fwd"
                        #         if(w > width/3):
                        #             print("Bwd")
                        #             self.moveCommand = "Bwd"
                        #         else:
                        #             print("Stop")
                        #             self.moveCommand = "Stop"

                    # def show_frame(self):
            cv2.imshow("frame", self.frame)
            key = cv2.waitKey(1) & 0xFF
            # cv2.waitKey(self.FPS_MS)

            # update the FPS counter
            self.fps.update()

        # time.sleep(self.FPS)

        # show the output self.frame

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    src = 0
    yolo = YOLO(src)
    print("started")
    # create irobot instance
    robot = iRobot()

    while True:
        try:
            yolo.update()
        except AttributeError:
            pass
        if(yolo.rotateCommand == "Right"):
            robot.turnRight(speed=0.03)
        elif(yolo.rotateCommand == "Left"):
            robot.turnLeft(speed=0.03)
        elif(yolo.rotateCommand == "Stop"):
            robot.turnRight(speed=0.0)  # Stop command not working.
            # robot.moveStop()
        elif(yolo.moveCommand == "Fwd"):
            robot.moveForward(speed=0.1)
        elif(yolo.moveCommand == "Bwd"):
            robot.moveBackwards(speed=0.1)
        elif(yolo.moveCommand == "Stop"):
            robot.moveForward(speed=0.0)  # Stop command not working.
            # robot.moveStop()

        # Wait for Esc key to stop
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
