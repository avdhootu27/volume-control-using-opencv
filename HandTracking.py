import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

# formality to use mediapipe
mpHands = mp.solutions.hands
# following class needs image only in RGB format
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()
    RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(RGBimg)
    #print(results.multi_hand_landmarks)     # to print x, y, z coordinates of detected hand

    # if hand detected
    if results.multi_hand_landmarks:
        for handLandMark in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLandMark, mpHands.HAND_CONNECTIONS)      # to show dots & lines on hand

    cv2.imshow("Image", img)

    cv2.waitKey(1)