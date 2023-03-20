# OpenCV program to detect face in real time
# import libraries of python OpenCV
# where its functionality resides

from lib.irobot_lib.iRobot import iRobot
import cv2
import numpy as np

# load the required trained XML classifiers
# https://github.com/Itseez/opencv/blob/master/
# data/haarcascades/haarcascade_frontalface_default.xml
# Trained XML classifiers describes some features of some
# object we want to detect a cascade function is trained
# from a lot of positive(faces) and negative(non-faces)
# images.
#face_cascade = cv2.CascadeClassifier(
 #   'lib/haarcascade/haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


# capture frames from a camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)

# create irobot instance

robot = iRobot()

show_cam = True

# Variables
deadZone = 100;


# loop runs if capturing has been initialized.
while True:

    # reads frames from a camera
    ret, img = cap.read()

    # convert to gray scale of each frames
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detects faces of different sizes in the input image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    height, width, rgb = np.shape(img)

    for (x, y, w, h) in faces:
        leftBoundary = x+w/2+deadZone/2
        rightBoundary = x+w/2-deadZone/2
        
        if( leftBoundary < width/2):
            print("go right")
            robot.turnRight(speed=0.1)
        elif( rightBoundary > width/2):
            print("go left")
            robot.turnLeft(speed=0.1)
        else:
            print("stop")
            robot.moveStop()

        if(show_cam):
            # To draw a rectangle in a face
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]

    # Display an image in a window
    if(show_cam):
        cv2.imshow('img', img)

    # Wait for Esc key to stop
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# Close the window
cap.release()

# De-allocate any associated memory usage
cv2.destroyAllWindows()
