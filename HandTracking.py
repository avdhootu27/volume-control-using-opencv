import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

# formality to use mediapipe
mpHands = mp.solutions.hands
# following class needs image only in RGB format
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

prevTime = 0
currTime = 0

while True:
    success, img = cap.read()
    RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(RGBimg)
    #print(results.multi_hand_landmarks)     # to print x, y, z coordinates of detected hand

    # if hand detected
    if results.multi_hand_landmarks:
        for handLandMark in results.multi_hand_landmarks:
            for id, lm in enumerate(handLandMark.landmark):
                height, width, channel = img.shape
                cx, cy = int(lm.x*width), int(lm.y*height)

            mpDraw.draw_landmarks(img, handLandMark, mpHands.HAND_CONNECTIONS)      # to show dots & lines on hand

    # showing FPS on image
    currTime = time.time()
    fps = 1/(currTime-prevTime)
    prevTime = currTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 2)

    cv2.imshow("Image", img)

    cv2.waitKey(1)