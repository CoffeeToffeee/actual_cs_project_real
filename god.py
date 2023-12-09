import cv2

cap = cv2.VideoCapture(1)

success , img = cap.read()
while True:
    cv2.imshow("caera", img)
