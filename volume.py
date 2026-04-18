import time

import autopy
import cv2
import numpy as np
import pyautogui

import HandTrackingModule as htm

# SETTINGS
wCam, hCam = 640, 480
frameR = 100
smoothening = 7

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

previous_vol = 50

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

while True:

    success, img = cap.read()
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)

    if len(lmList) != 0:

        fingers = detector.fingersUp()

        # =========================
        # MOVE MOUSE (INDEX ONLY)
        # =========================
        if fingers[1] == 1 and fingers[2] == 0:
            x1, y1 = lmList[8][1:]

            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            autopy.mouse.move(int(wScr - clocX), int(clocY))

            plocX, plocY = clocX, clocY

        # =========================
        # VOLUME CONTROL (THUMB + PINKY)
        # =========================
        if fingers == [1, 0, 0, 0, 1]:

            length, _, _ = detector.findDistance(4, 20, img)

            vol = np.interp(length, [20, 200], [0, 100])

            # CLEAN CONTROL (NO SPAM)
            if abs(vol - previous_vol) > 3:

                if vol > previous_vol:
                    pyautogui.press('volumeup')
                else:
                    pyautogui.press('volumedown')

                previous_vol = int(vol)

    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (20, 50),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("AI Virtual Mouse + Volume", img)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
