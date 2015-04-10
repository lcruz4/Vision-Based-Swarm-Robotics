import cv2
import numpy as np
import sys
import time

capture = cv2.VideoCapture()
capture.open(0)
maxf = open('./Maxs/maxs','r')
minf = open('./Maxs/mins','r')
maxh = maxf.readline()
maxs = maxf.readline()
maxv = maxf.readline()
minh = minf.readline()
mins = minf.readline()
minv = minf.readline()
upper = np.array([maxh,maxs,maxv], dtype=np.uint8)
lower = np.array([minh,mins,minv], dtype=np.uint8)
kern4 = np.ones((4,4),np.uint8)
kern2 = np.ones((2,2),np.uint8)
kern1 = np.ones((1,1),np.uint8)

ret, frame = capture.read()
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower, upper)
mask = cv2.erode(mask, kern2)
mask = cv2.dilate(mask, kern4)
mask = cv2.dilate(mask, kern4)
mom = cv2.moments(mask, True)
if(mom['m00']==0):
  xf = 120
  yf = 120
else:
  xf = int(mom['m10']/mom['m00'])
  yf = int(mom['m01']/mom['m00'])

r,h,c,w = yf-20, 40, xf-20, 40
track_window = (c,r,w,h)
roi = frame[yf-20:yf+20, xf-20:xf+20]
hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[40],[0,40])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
term_crit = (cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,10,1)

seq = []
tim = []
t = 0
while(1):
  ret, frame = capture.read()
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  roi = frame[yf-20:yf+20, xf-20:xf+20]
  hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  mask = cv2.inRange(hsv, lower, upper)
  mask = cv2.erode(mask, kern2)
  mask = cv2.dilate(mask, kern4)
  mask = cv2.dilate(mask, kern4)
  roi_hist = cv2.calcHist([hsv_roi],[0],mask,[40],[0,40])
  cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
#  mask = cv2.dilate(mask, kern2)
#  mask = cv2.dilate(mask, kern2)
#  mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kern1)
#  mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kern4)
  dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,40],1)
  dst = cv2.inRange(dst, np.array(150), np.array(255))
  ret, track_window = cv2.CamShift(dst,track_window,term_crit)

  box = cv2.cv.BoxPoints(ret)
  box = np.int0(box)
  l =  np.amin(box, axis=0)
  u =  np.amax(box, axis=0)
  cv2.rectangle(frame, tuple(l), tuple(u), (0,0,255), 0, 4)
  mom = cv2.moments(mask, True)
  if(mom['m00']==0):
    xf = 0
    yf = 0
    if(len(seq)>0):
      if(time.time() - t > .05*(len(seq)+1)+len(seq)*.05):
        seq.append(0)
        tim.append(time.time() - t)
  else:
    xf = int(mom['m10']/mom['m00'])
    yf = int(mom['m01']/mom['m00'])
    if(t == 0):
      t = time.time()
    if(time.time() - t > .05*(len(seq)+1)+len(seq)*.05):
      seq.append(1)
      tim.append(time.time() - t)
  cv2.circle(frame, (xf-2,yf-2), 1, (255,0,255), -1)
  cv2.circle(frame, (xf+2,yf-2), 1, (255,0,255), -1)
  cv2.circle(frame, (xf-2,yf+2), 1, (255,0,255), -1)
  cv2.circle(frame, (xf+2,yf+2), 1, (255,0,255), -1)
  cv2.namedWindow('frame', 0)
  cv2.imshow('frame',frame)
  cv2.imshow('bproj',dst)
  cv2.imshow('mask',mask)
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
