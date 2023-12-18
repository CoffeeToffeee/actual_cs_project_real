# Import modules
import cv2
import mediapipe as mp
import time as t
import pyautogui as pg
import math
import pygame

# Set the width and height of the screen
screen_width, screen_height = pg.size()

# Setting up the camera
cap = cv2.VideoCapture(2)
cap.set(3, screen_width)  # Set the width of the capture
cap.set(4, screen_height)  # Set the height of the capture

# Initialising mediapipe Hand modules
mpHands = mp.solutions.hands
hands = mpHands.Hands()
# Declaring other variables
lmList = []
pointer_mode = False
pinch_threshold = 45
cooldown = 0.05


# Creating functions
def sounds(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()


def toggle(thing):
    return not thing


def dist_thumb(landmark):
    if lmList and lmList[landmark] and lmList[4]:
        thumb_x, thumb_y = lmList[4][1], lmList[4][2]
        landmark_x, landmark_y = lmList[landmark][1], lmList[landmark][2]
        distance = math.sqrt(
            (landmark_x - thumb_x) ** 2 + (landmark_y - thumb_y) ** 2)  # distance of that landmark wrt to thumb
    if distance is None:
        distance = 0

    return distance


sounds("flappy/sounds/The bluetooth device is ready to pair Sound Effect.mp3")

while True:
    success, img = cap.read()
    # Mirror the image horizontally
    img = cv2.flip(img, 1)

    # Mediapipe uses RBG image
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Making mediapipe to process the image
    results = hands.process(imgRGB)

    # if the processing found results for landmarks
    if results.multi_hand_landmarks:
        for handLMS in results.multi_hand_landmarks:
            lmList = []  # Clear lmList at the beginning of each frame
            for id, lm in enumerate(handLMS.landmark):
                # Normalising the coordinates for the screen
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

    else:
        lmList = []

    if lmList and len(lmList) >= 20:
        # Moving cursor
        pg.moveTo(lmList[8][1], lmList[8][2], tween=pg.easeInOutQuad)

        # Checking for pointer only mode
        if dist_thumb(12) < pinch_threshold:
            pointer_mode = toggle(pointer_mode)
            sounds("flappy/sounds/GoPro Turn OnOff Sound Effect.mp3")
            if pointer_mode:
                print("Enabling pointer only mode")
            else:
                print("Disabling pointer only mode")
        # Conditions for pointer only mode
        if pointer_mode:
            t.sleep(cooldown)
            if dist_thumb(8) < pinch_threshold:
                print("Clicking")
                pg.click(button='right')  # Simulate clicking
        else:
            t.sleep(cooldown)
            if dist_thumb(8) < pinch_threshold:
                print("Clicking Space bar")
                pg.press('space')

            # if dist_thumb(20) < pinch_threshold:

            if dist_thumb(16) < pinch_threshold:
                print("Exiting")
                pg.press("esc")
                exit()
