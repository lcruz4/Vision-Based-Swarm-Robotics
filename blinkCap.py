import cv2
import numpy as np
import sys
import time

capture = cv2.VideoCapture()
capture.open(0)
upper = np.array([73,86,255], dtype=np.uint8)
lower = np.array([54,53,202], dtype=np.uint8)
seq = []
LEDcount = 0
rstcount = False
test = 0
while(1):
  ret, frame = capture.read()
  t = time.time()
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  mask = cv2.inRange(hsv, lower, upper)
  mom = cv2.moments(mask, True)
  if(mom['m00']==0):
    xf = 0
    yf = 0
    if(len(seq)>0):
      if(offTime == 0):
        offTime
      if(LEDcount!=0):
        if(LEDcount > 0.1):
          LEDcount = 0
      elif(LEDcount > 0.05):
        seq.append(0)
        rstcount = True
  else:
    xf = int(mom['m10']/mom['m00'])
    yf = int(mom['m01']/mom['m00'])
    if(onTime == 0):
      onTime = time.time()
    if(rstcount):
      if(time.time()-LEDcount >0.1):
        LEDcount = 0
        rstcount = False
    elif(time.time()-onTime > 0.05+*(len(seq)+1)):
      seq.append(1)
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
