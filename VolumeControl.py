import cv2
import time
import numpy as np
import HandModule as hdm

# initializing variables
camWidth, camHeight = 640, 480
pTime = 0

cap = cv2.VideoCapture(0)
cap.set(3, camWidth)
cap.set(4, camHeight)

while True:
    success, img = cap.read()


    # calculating fps
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Image",img)

    cv2.waitKey(1)