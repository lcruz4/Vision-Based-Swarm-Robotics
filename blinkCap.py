import cv2
import numpy as np
import sys
import time
from setup import *

while(1):
  ret, frame = capture.read()
  frame = cv2.warpPerspective(frame,M,(640,480))
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  roi = frame[ly:uy, lx:ux]
  hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  led_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
  ledmask = cv2.inRange(led_roi, ledlower, ledupper)

  redmask = cv2.inRange(hsv, redlower, redupper)
  redmask = cv2.erode(redmask, kern2)
  redmask = cv2.dilate(redmask, kern4)
  redmask = cv2.dilate(redmask, kern4)
  roi_hist = cv2.calcHist([hsv_roi],[0],redmask,[40],[0,40])
  cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
#  mask = cv2.dilate(mask, kern2)
#  mask = cv2.dilate(mask, kern2)
#  mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kern1)
#  mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kern4)
  ledmom = cv2.moments(ledmask, True)
  if(ledmom['m00']==0):
    xf = 0
    yf = 0
    if(len(seq)>0):
      if(time.time() - t > .05*(len(seq)+1)+len(seq)*.05):
        seq.append(0)
        tim.append(time.time() - t)
  else:
    xf = int(ledmom['m10']/ledmom['m00'])+lx
    yf = int(ledmom['m01']/ledmom['m00'])+ly
    print(xf,yf)
    if(t == 0):
      t = time.time()
    if(time.time() - t > .05*(len(seq)+1)+len(seq)*.05):
      seq.append(1)
      tim.append(time.time() - t)
  dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,40],1)
  dst = cv2.inRange(dst, np.array(150), np.array(255))
  ret, track_window = cv2.CamShift(dst,track_window,term_crit)

  box = cv2.cv.BoxPoints(ret)
  box = np.int0(box)
  lx,ly =  np.amin(box, axis=0)
  ux,uy =  np.amax(box, axis=0)
  cv2.rectangle(frame, (lx,ly), (ux,uy), (0,0,255), 0, 4)

  cv2.circle(frame, (xf-2,yf-2), 1, (255,0,255), -1)
  cv2.circle(frame, (xf+2,yf-2), 1, (255,0,255), -1)
  cv2.circle(frame, (xf-2,yf+2), 1, (255,0,255), -1)
  cv2.circle(frame, (xf+2,yf+2), 1, (255,0,255), -1)
  cv2.imshow('frame',frame)
  cv2.imshow('hsv',hsv)
  cv2.imshow('bproj',dst)
  cv2.imshow('mask',ledmask)
  if(len(seq) == 10):
    print(seq)
    print(tim)
    #break
  k = cv2.waitKey(5) & 0xFF
  if k == 27:
    break
print(seq)
print(tim)
cv2.destroyAllWindows()
