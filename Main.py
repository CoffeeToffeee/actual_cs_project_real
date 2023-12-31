# Import modules
import cv2
import mediapipe as mp
import time as t
import pyautogui as pg
import math

# Set the width and height of the screen
screen_width, screen_height = pg.size()

# Setting up the camera
cap = cv2.VideoCapture(2)
cap.set(3, screen_width)  # Set the width of the capture
cap.set(4, screen_height)  # Set the height of the capture

# Initialising mediapipe Hand modules

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
pTime = 0
cTime = 0
lmList = []
pointer_mode = False
Draw = True  # Used to draw the landmarks


def toggle(thing):
    thing = not thing


def dist_thumb(landmark):
    if lmList and lmList[landmark]:
        landmark_x, landmark_y = lmList[landmark][1], lmList[landmark][2]
        distance = math.sqrt(
            (landmark_x - thumb_x) ** 2 + (landmark_y - thumb_y) ** 2)  # distance of that landmark wrt to thumb


t.sleep(2)
use = input("What do you want to use the app for [game,spotify]: ")
while True:
    success, img = cap.read()
    # Mirror the image horizontally
    img = cv2.flip(img, 1)

    # Mediapipe uses RBG image
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLMS in results.multi_hand_landmarks:
            lmList = []  # Clear lmList at the beginning of each frame
            for id, lm in enumerate(handLMS.landmark):
                # Normalising the coordinates for the screen
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
            if Draw:
                mpDraw.draw_landmarks(img, handLMS, mpHands.HAND_CONNECTIONS)
    # Calculating the FPS
    cTime = t.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)

    cv2.imshow("Its you", img)

    if lmList:
        if lmList[8] != 0:
            if lmList[8][1] != 0 and lmList[8][2] != 0:
                #   print("Moving cursor to:", lmList[8][1], lmList[8][2] + 50)
                pg.moveTo(lmList[8][1], lmList[8][2])

            if lmList[8] and lmList[4] and lmList[20] and lmList[16] and lmList[12]:
                thumb_x, thumb_y = lmList[4][1], lmList[4][2]
                index_x, index_y = lmList[8][1], lmList[8][2]
                pinky_x, pinky_y = lmList[20][1], lmList[20][2]
                ring_x, ring_y = lmList[16][1], lmList[16][2]
                mid_x, mid_y = lmList[12][1], lmList[12][2]

                distance_index = math.sqrt((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2)  # index thumb
                distance_pinky = math.sqrt((pinky_x - thumb_x) ** 2 + (pinky_y - thumb_y) ** 2)  # index pinky
                distance_ring = math.sqrt((ring_x - thumb_x) ** 2 + (ring_y - thumb_y) ** 2)  # ring and thumb
                distance_middle = math.sqrt((mid_x - thumb_x) ** 2 + (mid_y - thumb_y) ** 2)
                pinch_threshold = 40

            if use == "spotify":
                if not pointer_mode:
                    if distance_index < pinch_threshold:
                        print("Play/Pause")
                        pg.press('space')  # Simulate pressing the spacebar for play/pause

                    if distance_pinky < pinch_threshold:
                        print("Skipping track")
                        pg.hotkey('command', 'right')  # Simulate pressing Command + right arrow for skipping track

                if distance_ring < pinch_threshold:
                    print("Exiting")
                    exit()

                if distance_middle < pinch_threshold:
                    toggle(pointer_mode)
                    if pointer_mode:
                        print("Enabling pointer only mode")
                    else:
                        print("Disabling pointer only mode")


            elif use == "game":
                if not pointer_mode:
                    if distance_index < pinch_threshold:
                        print("Clicking Space bar")
                        pg.press('space')

                    if distance_pinky < pinch_threshold:
                        print("Pressing escape")
                        pg.press("esc")

                if distance_ring < pinch_threshold:
                    print("Exiting")
                    pg.press("esc")
                    exit()

                if distance_middle < pinch_threshold:
                    toggle(pointer_mode)
                    if pointer_mode:
                        print("Enabling pointer only mode")
                    else:
                        print("Disabling pointer only mode")
            else:
                print("Invalid input")
                exit()
