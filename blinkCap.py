import cv2
import numpy as np
import sys
import time

def onmouse(event, x, y, flags, param):
  if flags & cv2.EVENT_FLAG_LBUTTON:
    global clickCount, t00, t01, t10, t11
    if clickCount == 0:
      t00 = [x,y]
      print(t00)
    elif clickCount == 1:
      t01 = [x,y]
      print(t01)
    elif clickCount == 2:
      t10 = [x,y]
      print(t10)
    elif clickCount == 3:
      t11 = [x,y]
      print(t11)
    else:
      pass
    clickCount = clickCount + 1
cv2.namedWindow('frame', 0)
cv2.setMouseCallback("frame", onmouse)
clickCount = 0
t00 = []
t01 = []
t10 = []
t11 = []
capture = cv2.VideoCapture()
capture.open(0)
redmax = open('redMaxs','r')
redmin = open('redMins','r')
ledmax = open('ledMaxs','r')
ledmin = open('ledMins','r')
redmaxh = redmax.readline()
redmaxs = redmax.readline()
redmaxv = redmax.readline()
redminh = redmin.readline()
redmins = redmin.readline()
redminv = redmin.readline()
ledmaxh = ledmax.readline()
ledmaxs = ledmax.readline()
ledmaxv = ledmax.readline()
ledminh = ledmin.readline()
ledmins = ledmin.readline()
ledminv = ledmin.readline()
redmax.close()
redmin.close()
ledmax.close()
ledmin.close()
redupper = np.array([redmaxh,redmaxs,redmaxv], dtype=np.uint8)
redlower = np.array([redminh,redmins,redminv], dtype=np.uint8)
ledupper = np.array([ledmaxh,ledmaxs,ledmaxv], dtype=np.uint8)
ledlower = np.array([ledminh,ledmins,ledminv], dtype=np.uint8)
kern4 = np.ones((4,4),np.uint8)
kern2 = np.ones((2,2),np.uint8)
kern1 = np.ones((1,1),np.uint8)

#ret, frame = capture.read()
while clickCount<4:
  ret, frame = capture.read()
  cv2.imshow('frame',frame)
  k = cv2.waitKey(5) & 0xFF
  if k == 27:
    break
tpts = np.float32([t00,t01,t10,t11])
npts = np.float32([[0,0],[640,0],[0,480],[640,480]])
M = cv2.getPerspectiveTransform(tpts,npts)
frame = cv2.warpPerspective(frame,M,(640,480))

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
redmask = cv2.inRange(hsv, redlower, redupper)
redmask = cv2.erode(redmask, kern2)
redmask = cv2.dilate(redmask, kern4)
redmask = cv2.dilate(redmask, kern4)

redmom = cv2.moments(redmask, True)
if(redmom['m00']==0):
  xf = 120
  yf = 120
else:
  xf = int(redmom['m10']/redmom['m00'])
  yf = int(redmom['m01']/redmom['m00'])

lx,ly,ux,uy = [xf-20,yf-20,xf+20,yf+20]
print(lx,ly,ux,uy)
r,h,c,w = ly, 40, lx, 40
track_window = (c,r,w,h)
roi = frame[ly:uy, lx:ux]
hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
roi_hist = cv2.calcHist([hsv_roi],[0],redmask,[40],[0,40])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
term_crit = (cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,10,1)

seq = []
tim = []
t = 0
cv2.namedWindow('hsv', 0)
cv2.namedWindow('bproj', 0)
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
