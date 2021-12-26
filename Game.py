import cv2
import time
import HandModule as hdm

cap = cv2.VideoCapture(0)
prevTime = 0
currTime = 0

detector = hdm.handDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPositions(img)

    # showing FPS on image
    currTime = time.time()
    fps = 1 / (currTime - prevTime)
    prevTime = currTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

