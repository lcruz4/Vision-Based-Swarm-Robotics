import cv2
import numpy as np
import sys
import time

capture = cv2.VideoCapture()
capture.open(0)
upper = np.array([90,18,255], dtype=np.uint8)
lower = np.array([0,0,254], dtype=np.uint8)
seq = []
t = time.time()
while(1):
  ret, frame = capture.read()
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  mask = cv2.inRange(hsv, lower, upper)
  mom = cv2.moments(mask, True)
  if(mom['m00']==0):
    xf = 0
    yf = 0
    if(len(seq)>0):
      print(str(time.time()-t))
      dt = time.time()-t
      while(time.time()-t<.1-dt):
        continue
      seq.append(0)
      t = time.time()
  else:
    xf = int(mom['m10']/mom['m00'])
    yf = int(mom['m01']/mom['m00'])
    print(str(time.time()-t))
    dt = time.time()-t
    while(time.time()-t<.1-dt):
      continue
    seq.append(1)
    t = time.time()
  if(len(seq)==0):
    t = time.time()
  cv2.circle(frame, (xf-2,yf-2), 1, (255,0,255), -1)
  cv2.circle(frame, (xf+2,yf-2), 1, (255,0,255), -1)
  cv2.circle(frame, (xf-2,yf+2), 1, (255,0,255), -1)
  cv2.circle(frame, (xf+2,yf+2), 1, (255,0,255), -1)
  cv2.namedWindow('frame', 0)
  cv2.imshow('frame',frame)
  cv2.imshow('mask',mask)
  if(len(seq) == 10):
    break
  k = cv2.waitKey(5) & 0xFF
  if k == 27:
    break
print(seq)
cv2.destroyAllWindows()
