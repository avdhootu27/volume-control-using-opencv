import cv2
import time
import numpy as np
import HandModule as hdm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# initializing variables
camWidth, camHeight = 640, 480
pTime = 0

cap = cv2.VideoCapture(0)
cap.set(3, camWidth)
cap.set(4, camHeight)

# creating objects of hand detector class
detector = hdm.handDetector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volumeRange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(0, None)

minVol = volumeRange[0]
maxVol = volumeRange[1]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPositions(img, draw=False)

    if len(lmList) != 0:        # draw circles
        # print(lmList[4], lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 4, (0, 0, 255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (0, 0, 255), 2)

        length = math.hypot(x2 - x1, y2 - y1)
        if length<30:
            cv2.circle(img, (cx, cy), 4, (0, 255, 0), cv2.FILLED)

        vol = np.interp(length, [50,220], [minVol, maxVol])
        # print(length, vol)
        volume.SetMasterVolumeLevel(vol, None)

    # calculating fps
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Image",img)

    cv2.waitKey(1)

# volBar = 150
# volPer = 100
# volBar = np.interp(vol, [minVol, maxVol], [400, 150])
# volPer = np.interp(vol, [minVol, maxVol], [0, 100])
# drawing volume level
# cv2.rectangle(img, (50,150), (85,400), (0, 255, 0), 3)
# cv2.rectangle(img, (50,int(volBar)), (85,400), (0, 255, 0), cv2.FILLED)
# cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)