import pyautogui

import HandTrackingModule as htm
import cv2
import pyautogui as pg
import time as t
import math
import sys

pTime = 0
cTime = 0

# Change the value in video capture to 0,1,2 depending on which camera you are using
cap = cv2.VideoCapture(0)
detector = htm.handDetector()


def run():
    global cTime, pTime

    while True:
        success, img = cap.read()
        img = detector.findHands(img, draw=True)  # Detects hands and marks lines
        lmList = detector.findPosition(img, draw=True)  # Finds landmarks on the hand and draws dots

        # Code for calculating FPS
        cTime = t.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)

        # Displaying our camera:
        cv2.imshow("Image", img)
        cv2.waitKey(1)

        # moving and clicking part:
        if lmList:
            if lmList[8] != 0:
                if lmList[8][1] != 0 and lmList[8][2] != 0:
                    pg.moveTo(lmList[8][1], lmList[8][2], 2)
                if lmList[8] and lmList[4] and lmList[20]:
                    # Calculate distance between thumb and index finger
                    thumb_x, thumb_y = lmList[4][1], lmList[4][2]
                    index_x, index_y = lmList[8][1], lmList[8][2]
                    pinky_x, pinky_y = lmList[20][1], lmList[20][2]

                    # Calculating the distances
                    distance_thumb = math.sqrt((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2)
                    distance_pinky = math.sqrt((index_x - pinky_x) ** 2 + (index_y - pinky_y) ** 2)
                    # Set a distance threshold for pinching
                    pinch_threshold = 50

                    if distance_thumb < pinch_threshold:
                        pg.click()

                    if distance_pinky < pinch_threshold:
                        pyautogui.keyDown('esc')
                        sys.exit()
