import cv2
import mediapipe as mp
import math
from ctypes import cast, POINTER
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import tkinter as tk
from tkinter import simpledialog

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]


class HandDetector:
    def __init__(self, mode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)

        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)
        if self.result.multi_hand_landmarks:
            for handLMS in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLMS, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []

        if self.result.multi_hand_landmarks:

            myhand = self.result.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])

        return self.lmList

    def fingersUp(self):
        finger = []

        if self.lmList != []:
            if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
                finger.append(0)
            else:
                finger.append(1)

            for id in range(1, 5):
                if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                    finger.append(1)
                else:
                    finger.append(0)

        return finger

    def Distance(self, img, Top_1, Top_2, draw=True):
        x1, y1 = self.lmList[Top_1][1:]
        x2, y2 = self.lmList[Top_2][1:]

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        length = math.hypot(x1 - x2, y1 - y2)

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 8), 2)
            cv2.circle(img, (cx, cy), 7, (8, 0, 255), cv2.FILLED)

        return length, img, [x1, y1, x2, y2, cx, cy]


def main():
    detector = HandDetector()
    # initialize local volume variables so they're defined even when no hand is detected
    vol = 0
    volBar = 400
    volPer = 0

    root = tk.Tk()
    root.withdraw()  # κρύβει το main window

    length_value_multiplier = simpledialog.askfloat(
        "Length Multiplier",
        "Enter value (e.g. 3 for sensitive, 4 for less):"
    )

    if length_value_multiplier is not None:
        length_selected = True

    if length_selected:
        while True:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            img = detector.findHands(img)
            lmList = detector.findPosition(img)

            if lmList != ([]):
                length, img, [x1, y1, x2, y2, cx, cy] = detector.Distance(img, 4, 8, draw = True)
                length = length * length_value_multiplier
                # Hand range 50-300
                #Volume range -65 - 0

                vol = np.interp(length, [50 ,300], [minVol, maxVol])
                volBar = np.interp(length, [50, 300], [400,150])
                volPer = np.interp(length, [50, 300], [0,100])
                print(int(length), vol)
                volume.SetMasterVolumeLevel(vol, None)


            cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
            cv2.putText(img, f'{int(volPer)}'+'%', (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            cv2.imshow("output", img)

            if cv2.waitKey(1) == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
