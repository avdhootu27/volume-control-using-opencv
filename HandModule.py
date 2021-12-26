import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands = 2, complexity = 1, detectionConf = 0.5, trackingConf = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionConf = detectionConf
        self.trackingConf = trackingConf

        self.mpHands = mp.solutions.hands       # formality to use mediapipe
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, self.detectionConf, self.trackingConf)       # this class needs image only in RGB format
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(RGBimg)
        # print(results.multi_hand_landmarks)     # to print x, y, z coordinates of detected hand

        # if hand detected
        if self.results.multi_hand_landmarks:
            for handLandMark in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLandMark, self.mpHands.HAND_CONNECTIONS)  # to show dots & lines on hand
        return img

    def findPositions(self, img, handNumber = 0, draw = True):
        lmList = []
        if self.results.multi_hand_landmarks:
            handLandMark = self.results.multi_hand_landmarks[handNumber]
            for id, lm in enumerate(handLandMark.landmark):
                height, width, channel = img.shape
                cx, cy = int(lm.x * width), int(lm.y * height)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)
        return lmList

def main():
    cap = cv2.VideoCapture(0)
    prevTime = 0
    currTime = 0

    detector = handDetector()

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

if __name__ == "__main__":
    main()