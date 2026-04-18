import os
import time

import autopy
import cv2
import numpy as np

import HandTrackingModule as htm

wCam, hCam = 640, 480
frameR = 100
smoothening = 7

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) == 0:
        continue

    x1, y1 = lmList[8][1:]
    x2, y2 = lmList[12][1:]

    fingers = detector.fingersUp()

    cv2.rectangle(img, (frameR, frameR),
                  (wCam - frameR, hCam - frameR),
                  (255, 0, 255), 2)

    if fingers[1] == 1 and fingers[2] == 0:
        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening

        autopy.mouse.move(int(wScr - clocX), int(clocY))
        plocX, plocY = clocX, clocY

    elif fingers[1] == 1 and fingers[2] == 1:
        length, img, lineInfo = detector.findDistance(8, 12, img)

        if length < 40:
            autopy.mouse.click()

    elif fingers[0] == 1 and fingers[1] == 1:
        length, img, lineInfo = detector.findDistance(4, 8, img)

        if length < 40:
            autopy.mouse.click(button=autopy.mouse.Button.RIGHT)

    elif fingers == [1, 0, 0, 0, 1]:
        length, img, lineInfo = detector.findDistance(4, 20, img)

        if length < 40:
            os.startfile("A:\\")

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (20, 50),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("AI Virtual Mouse", img)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
