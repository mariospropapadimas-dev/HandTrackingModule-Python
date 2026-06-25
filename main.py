import cv2
import numpy as np
from pycaw.pycaw import AudioUtilities
import tkinter as tk
from tkinter import simpledialog
from hand_detector import HandDetector

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Initialize audio control
devices = AudioUtilities.GetSpeakers()
volume = devices.EndpointVolume
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]


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

    length_selected = length_value_multiplier is not None

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
