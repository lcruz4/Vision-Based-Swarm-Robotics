import cv2
import numpy as np
from socket import *

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

kern1 = np.ones((1,1),np.uint8)
kern2 = np.ones((2,2),np.uint8)
kern4 = np.ones((4,4),np.uint8)
kern8 = np.ones((8,8),np.uint8)
kern16= np.ones((16,16),np.uint8)
kern16= np.ones((16,16),np.uint8)
clickCount = 0
t00 = []
t01 = []
t10 = []
t11 = []
ips = ['10.159.154.80','10.159.135.64','10.159.9.3']
locs= [[],[],[]]
cv2.namedWindow('frame', 0)
cv2.setMouseCallback("frame", onmouse)
capture = cv2.VideoCapture()
capture.open(0)
redmax = open('./Maxs/redMaxs','r')
redmin = open('./Maxs/redMins','r')
redmaxh = redmax.readline()
redmaxs = redmax.readline()
redmaxv = redmax.readline()
redminh = redmin.readline()
redmins = redmin.readline()
redminv = redmin.readline()
redmax.close()
redmin.close()
redupper = np.array([redmaxh,redmaxs,redmaxv], dtype=np.uint8)
redlower = np.array([redminh,redmins,redminv], dtype=np.uint8)

while clickCount<4:
  ret, frame = capture.read()
  cv2.imshow('frame',frame)
  k = cv2.waitKey(5) & 0xFF
  if k == 27:
    break
tpts = np.float32([t00,t01,t10,t11])
npts = np.float32([[0,0],[640,0],[0,480],[640,480]])
M = cv2.getPerspectiveTransform(tpts,npts)
count = 0
while(1):
  ret, frame = capture.read()
  frame = cv2.warpPerspective(frame,M,(640,480))
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

  redupper = np.array([redmaxh,redmaxs,redmaxv], dtype=np.uint8)
  redlower = np.array([redminh,redmins,redminv], dtype=np.uint8)
  maskred = cv2.inRange(hsv, redlower, redupper)
  maskred = cv2.morphologyEx(maskred,cv2.MORPH_CLOSE,kern16)
  cv2.imshow('maskred',maskred)
  c,x=cv2.findContours(maskred,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  for i in c:
    xf = sum(i[:,0,0])/len(i[:,0,0])
    yf = sum(i[:,0,1])/len(i[:,0,1])
    cv2.circle(frame, (xf,yf), 2, (255,0,0), -1)
    rNum = 9
    if(xf < 100 and yf < 100 and locs[0] == []):
      rNum = 0
    elif(xf > 500 and yf < 100 and locs[1] == []):
      rNum = 1
    elif(locs[2] == []):
      rNum = 2
    for j in range(3):
      if(locs[j] != []):
        dif = [xf-locs[j][0],yf-locs[j][1]]
        if(dif[0]<20 and dif[0]>-20 and dif[1]<20 and dif[1]>-20):
          rNum = j
          xf = (xf + locs[j][0])/2
          yf = (yf + locs[j][1])/2
    print("robot%d loc (x,y): (%f,%f)" % (rNum+1,xf,yf))
    locs[rNum]=[xf,yf]
    count = count + 1
  count = 0
  cv2.circle(frame, (577,143), 2, (0,255,0), -1)
  cv2.circle(frame, (340,100), 2, (0,0,255), -1)
  frame = cv2.resize(frame, (0,0), fx=2, fy=2)
  cv2.imshow('frame', frame)
  k = cv2.waitKey(5) & 0xFF
  if k == 27:
    break

cv2.destroyAllWindows()
