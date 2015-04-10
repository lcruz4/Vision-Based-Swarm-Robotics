import cv2
import numpy as np
from socket import *
from connSetup import *

task = "circle 320,240 50"

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
ipF = open('ips','r')
ips = []
tlist = []
for line in ipF:
  tlist.append(line[:-1])
  if(len(tlist)==2):
    ips.append(tlist)
    tlist = []
locs= {'r1':[],'r2':[],'r3':[]}
cv2.namedWindow('frame', 0)
cv2.setMouseCallback("frame", onmouse)
capture = cv2.VideoCapture()
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))
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

for soc in csoc:
  csoc[soc].send(task.encode())

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
    rName = '?'
    if(count == 0):
      if(xf < 320 and yf < 240 and locs['r1'] == []):
        rName = 'r1'
      elif(xf > 320 and yf < 240 and locs['r3'] == []):
        rName = 'r3'
      elif(locs['r2'] == []):
        rName = 'r2'
      else:
        continue
    else:
      for name in locs:
        if(locs[name][0]-xf < 20 and locs[name][1]-yf < 20):
          rName = name
      if(rName == '?'):
        continue
    for name in locs:
      if(locs[name]!=[]):
        dif = [xf-locs[name][0],yf-locs[name][1]]
        if(dif[0]<20 and dif[0]>-20 and dif[1]<20 and dif[1]>-20):
          rName = name
          xf = (xf + locs[name][0])/2
          yf = (yf + locs[name][1])/2
    print("robot"+rName+" loc (x,y): (%f,%f)" % (xf,yf))
    locs[rName]=[xf,yf]
  if(count%10 == 0):
    for soc in csoc:
      locxy = locs[soc]
      locxy[0] = int(locxy[0])
      locxy[1] = int(locxy[1])
      strx = str(locxy[0])
      stry = str(locxy[1])
      while(len(strx)<3):
        strx = "0"+strx
      while(len(stry)<3):
        stry = "0"+stry

      csoc[soc].send((strx+","+stry).encode())

  cv2.circle(frame, (577,143), 2, (0,255,0), -1)
  cv2.circle(frame, (340,100), 2, (0,0,255), -1)
  cv2.circle(frame, (XMAX/2,YMAX/2), 40, (255,0,0), 1)
  frame = cv2.resize(frame, (0,0), fx=2, fy=2)
  cv2.imshow('frame', frame)
  k = cv2.waitKey(5) & 0xFF
  count = count + 1
  if k == 27:
    break

cv2.destroyAllWindows()
