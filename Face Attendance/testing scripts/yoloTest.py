from ultralytics import YOLO
import cvzone
import math
import cv2
import time
import numpy as np


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


model = YOLO("")

classesFile = 'coco.names'
classNames = []

with open(classesFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')
print(classNames)


while True:

    success, img = cap.read()
    cv2.imshow('image', img)
    cv2.waitKey(1)