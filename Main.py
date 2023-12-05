import cv2
import mediapipe as mp
import time as t
import pyautogui as pg
import math

# Set the width and height of the screen
screen_width, screen_height = pg.size()

# Setting up the camera
cap = cv2.VideoCapture(0)
cap.set(3, screen_width)  # Set the width of the capture
cap.set(4, screen_height)  # Set the height of the capture

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
pTime = 0
cTime = 0
lmList = []
Draw = True

while True:
    success, img = cap.read()

    # Mirror the image horizontally
    img = cv2.flip(img, 1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLMS in results.multi_hand_landmarks:
            lmList = []  # Clear lmList at the beginning of each frame
            for id, lm in enumerate(handLMS.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
            if Draw:
                mpDraw.draw_landmarks(img, handLMS, mpHands.HAND_CONNECTIONS)

    cTime = t.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)

    cv2.imshow("Hey its you!", img)

    # Print statements for debugging
    print("lmList:", lmList)

    if lmList:
        if lmList[8] != 0:
            if lmList[8][1] != 0 and lmList[8][2] != 0:
                print("Moving cursor to:", lmList[8][1], lmList[8][2])
                pg.moveTo(lmList[8][1], lmList[8][2])

            if lmList[8] and lmList[4] and lmList[20]:
                thumb_x, thumb_y = lmList[4][1], lmList[4][2]
                index_x, index_y = lmList[8][1], lmList[8][2]
                pinky_x, pinky_y = lmList[20][1], lmList[20][2]

                distance_thumb = math.sqrt((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2)
                distance_pinky = math.sqrt((index_x - pinky_x) ** 2 + (index_y - pinky_y) ** 2)
                pinch_threshold = 50

                if distance_thumb < pinch_threshold:
                    print("Clicking")
                    pg.click()

                # Check if distance_pinky is below the threshold
                if distance_pinky < pinch_threshold:
                    print("Exiting the code")
                    break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
