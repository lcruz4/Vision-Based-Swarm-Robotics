import cv2
import numpy as np
import sys

capture = cv2.VideoCapture()
capture.open(0)

nx = 640
ny = 480

kernel = np.ones((2,2),np.uint8)

while(1):
    #frame = np.zeros((nx,ny,3), np.uint8)
    ret, frame = capture.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#    106 63, 225 175
    upper_white = np.array([54,125,255], dtype=np.uint8)
    lower_white = np.array([46,25,150], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_white, upper_white)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    #mask = cv2.dilate(mask, kernel)
    mom = cv2.moments(mask, True)
    if(mom['m00']==0):
      xf = 0
      yf = 0
    else:
      xf = int(mom['m10']/mom['m00'])
      yf = int(mom['m01']/mom['m00'])
      #print(hsv[yf,xf])
    cv2.circle(frame, (xf-2,yf-2), 1, (255,0,255), -1)
    cv2.circle(frame, (xf+2,yf-2), 1, (255,0,255), -1)
    cv2.circle(frame, (xf-2,yf+2), 1, (255,0,255), -1)
    cv2.circle(frame, (xf+2,yf+2), 1, (255,0,255), -1)
    cv2.circle(frame, (145,155), 1, (255,0,255), -1)
    cv2.circle(frame, (155,155), 1, (255,0,255), -1)
    cv2.circle(frame, (145,165), 1, (255,0,255), -1)
    cv2.circle(frame, (155,165), 1, (255,0,255), -1)
    cv2.circle(mask, (145,155), 1, (255,0,255), -1)
    cv2.circle(mask, (155,155), 1, (255,0,255), -1)
    cv2.circle(mask, (145,165), 1, (255,0,255), -1)
    cv2.circle(mask, (155,165), 1, (255,0,255), -1)
    cv2.namedWindow('frame', 0)
    cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
