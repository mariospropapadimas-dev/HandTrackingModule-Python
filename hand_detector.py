import cv2
from mediapipe.python.solutions import hands, drawing_utils
from math import hypot

class HandDetector:
    def __init__(self, mode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.hands = hands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)
        if self.result.multi_hand_landmarks:
            for handLMS in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLMS, hands.HAND_CONNECTIONS)

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

        length = hypot(x1 - x2, y1 - y2)

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 8), 2)
            cv2.circle(img, (cx, cy), 7, (8, 0, 255), cv2.FILLED)

        return length, img, [x1, y1, x2, y2, cx, cy]

