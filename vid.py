import cv2
import numpy as np
import sys
import time

cv2.namedWindow("img", 0)
capture = cv2.VideoCapture()
capture.open(0)

while(1):
    ret, frame = capture.read()
    cv2.imshow("img",frame)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
