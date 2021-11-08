import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=1)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = ""

keyboard = Controller()
def drawAll(img, buttonList):
     imgNew = np.zeros_like(img, np.uint8)
     for button in buttonList:
         x, y = button.pos
         cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                           20, rt=0)
         cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
                       (255, 0, 255), cv2.FILLED)
         cv2.putText(imgNew, button.text, (x + 40, y + 60),
                     cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)

     out = img.copy()
     alpha = 0.5
     mask = imgNew.astype(bool)
     print(mask.shape)
     out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
     return out

class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text
      
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)
