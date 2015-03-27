import cv2
import numpy as np

capture = cv2.VideoCapture()
capture.open(0)
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

newx = 320
newy = 240

nx = 640
ny = 480

while(1):
    frame = np.zeros((newx,newy,3), np.uint8)
    ret, frame = capture.read()
#    frameBGR = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of white color in HSV
    # change it according to your need !
    # blue
    minh = 78
    mins = 3
    minv = 238
    maxh = 106
    maxs = 24
    maxv = 255
    upper_white = np.array([maxh,maxs,maxv], dtype=np.uint8)
    lower_white = np.array([minh,mins,minv], dtype=np.uint8)

    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv, lower_white, upper_white)
    # Bitwise-AND mask and original image
    mom = cv2.moments(mask, True)
    xf = 0
    yf = 0
    if(mom['m00']!=0):
      xf = int(mom['m10']/mom['m00'])
      yf = int(mom['m01']/mom['m00'])
    cv2.circle(frame, (xf,yf), 3, (255,0,255), -1)
    out.write(frame)
    cv2.imshow('frame',frame)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
