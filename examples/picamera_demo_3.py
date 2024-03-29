from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 40)
start = time.time()
for i in range(400):
    ret, img = cap.read()
    cv2.imshow('Picamera', img)
    if cv2.waitKey(1) == 27:
        break  # esc to quit
