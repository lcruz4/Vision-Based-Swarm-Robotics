import cv2
import numpy as np
import time
import math
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
ledlocs = []
tlist = []
cv2.namedWindow('frame', 0)
cv2.setMouseCallback("frame", onmouse)
capture = cv2.VideoCapture()
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))
capture.open(0)
redmax = open('./Maxs/redMaxs','r')
redmin = open('./Maxs/redMins','r')
ledmax = open('./Maxs/ledMaxs','r')
ledmin = open('./Maxs/ledMins','r')
ledmaxh = ledmax.readline()
ledmaxs = ledmax.readline()
ledmaxv = ledmax.readline()
ledminh = ledmin.readline()
ledmins = ledmin.readline()
ledminv = ledmin.readline()
redmaxh = redmax.readline()
redmaxs = redmax.readline()
redmaxv = redmax.readline()
redminh = redmin.readline()
redmins = redmin.readline()
redminv = redmin.readline()
redmax.close()
redmin.close()
ledmax.close()
ledmin.close()
redupper = np.array([redmaxh,redmaxs,redmaxv], dtype=np.uint8)
redlower = np.array([redminh,redmins,redminv], dtype=np.uint8)
seqs = []
locs= {}
for ipname in IPlist:
  locs[ipname[1]] = []
  s = ipname[0].split('.')
  seqs.append(int(s[-1]))
ledseq = [0,0,0,0,0]
ledbit = [0,0,0,0,0]
t = []
ledoff = []

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
ledc = 0
seqsDone = 0

for soc in csoc:
  csoc[soc].send(task.encode())
  print("task send to "+soc)#DEBUG

while(seqsDone < iplen):
  ret, frame = capture.read()
  frame = cv2.warpPerspective(frame,M,(640,480))
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  ledupper = np.array([ledmaxh,ledmaxs,ledmaxv], dtype=np.uint8)
  ledlower = np.array([ledminh,ledmins,ledminv], dtype=np.uint8)
  maskled = cv2.inRange(hsv, ledlower, ledupper)
  maskled = cv2.morphologyEx(maskled,cv2.MORPH_CLOSE,kern1)
  c,x=cv2.findContours(maskled,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  ccount = 1
  print("--------------------------")
  for i in range(len(ledoff)):
    ledoff[i] = True
  for i in c:
    ledc = -1
    xf = sum(i[:,0,0])/len(i[:,0,0])
    yf = sum(i[:,0,1])/len(i[:,0,1])
    for i in range(len(ledlocs)):	#check if loc already saved
      if(math.fabs(ledlocs[i][0]-xf) < 10
	and math.fabs(ledlocs[i][1]-yf) < 10):
        ledc = i
        print("led "+str(ledc)+"on")#DEBUG
    if(ccount > 5):
      print("NOISE:")#DEBUG
      print([xf,yf])
      break
    elif(ledc==-1):	#new led
      ledoff.append(False)
      ledc = len(ledlocs)
      ledlocs.append([xf,yf])
      t.append(time.time())
      print("led "+str(ledc)+" started at loc "+str(xf)+","+str(yf))#DEBUG
    if(time.time() - t[ledc] > .05*(2*ledbit[ledc]+3)):
      ledseq[ledc] = ledseq[ledc]+(128>>ledbit[ledc])
      print("bit "+str(7-ledbit[ledc])+" on led "+str(ledc)+" HIGH")#DEBUG
      print("seq "+str(ledseq[ledc])+" on led "+str(ledc))#DEBUG
      ledbit[ledc] = ledbit[ledc] + 1
    ledoff[ledc] = False
    ccount = ccount + 1
  for c in range(len(ledoff)):
    if(ledoff[c] and ledbit[c]<8):
      print("led "+str(c)+" off")#DEBUG
      if(time.time() - t[c] > .05*(2*ledbit[c]+3)):
        print("bit "+str(8-ledbit[c])+" on led "+str(c)+" LOW")#DEBUG
        ledbit[c] = ledbit[c] + 1

  for bit in ledbit:
    if(bit == 8):
      seqsDone = seqsDone + 1

  cv2.imshow('frame', frame)
  k = cv2.waitKey(5) & 0xFF
  count = count + 1
  if k == 27:
    break

c = 0
for name in locs:
  for i in range(len(seqs)):
    if(ledseq[i] == seqs[c]):
      locs[name] = ledloc[i]
      print("led "+i+" matches seq of "+name)
      break
  c = c + 1

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
    for name in locs:
      if(locs[name][0]-xf < 20 and locs[name][1]-yf < 20):
        rName = name
    if(rName == '?'):
      continue
    for name in locs:
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
