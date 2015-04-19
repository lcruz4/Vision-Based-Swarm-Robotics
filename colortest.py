import cv2
import numpy as np
import sys
import time
cv2.namedWindow("img", 0)

capture = cv2.VideoCapture()
capture.open(0)
t = time.time()
freq = 999999999999999999

f1 = open('./Maxs/'+sys.argv[1]+'Mins', 'r')
f2 = open('./Maxs/'+sys.argv[1]+'Maxs', 'r')
maxh = f2.readline()
maxs = f2.readline()
maxv = f2.readline()
minh = f1.readline()
mins = f1.readline()
minv = f1.readline()
counter = 0
while(1):
    ret, frame = capture.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_thresh = np.array([minh,mins,minv], dtype=np.uint8)
    upper_thresh = np.array([maxh,maxs,maxv], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_thresh, upper_thresh)
    mom = cv2.moments(mask, True)
    if(mom['m00']!=0):
      xf = int(mom['m10']/mom['m00'])
      yf = int(mom['m01']/mom['m00'])
      cv2.circle(frame, (xf,yf), 1, (255,0,255), -1)

    cv2.imshow("img",frame)
    cv2.imshow("mask",mask)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
