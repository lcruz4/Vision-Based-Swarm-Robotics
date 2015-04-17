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
out2= cv2.VideoWriter('output2.avi',fourcc, 20.0, (640,480))
capture.open(0)
redmax = open('./Maxs/redMaxs','r')
redmin = open('./Maxs/redMins','r')
ledmax = open('./Maxs/ledMaxs','r')
ledmin = open('./Maxs/ledMins','r')
blumax = open('./Maxs/blueMaxs','r')
blumin = open('./Maxs/blueMins','r')
blkmax = open('./Maxs/blackMaxs','r')
blkmin = open('./Maxs/blackMins','r')
blkmaxh = blkmax.readline()
blkmaxs = blkmax.readline()
blkmaxv = blkmax.readline()
blkminh = blkmin.readline()
blkmins = blkmin.readline()
blkminv = blkmin.readline()
blumaxh = blumax.readline()
blumaxs = blumax.readline()
blumaxv = blumax.readline()
bluminh = blumin.readline()
blumins = blumin.readline()
bluminv = blumin.readline()
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
blumax.close()
blumin.close()
blkmax.close()
blkmin.close()
redupper = np.array([redmaxh,redmaxs,redmaxv], dtype=np.uint8)
redlower = np.array([redminh,redmins,redminv], dtype=np.uint8)
seqs = []
locs= {}
bluloc = {}
blkloc = {}
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
  out.write(frame)
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
  seqsDone = 0
  ret, frame = capture.read()
  frame = cv2.warpPerspective(frame,M,(640,480))
  out.write(frame)
  out2.write(frame)
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  ledupper = np.array([ledmaxh,ledmaxs,ledmaxv], dtype=np.uint8)
  ledlower = np.array([ledminh,ledmins,ledminv], dtype=np.uint8)
  maskled = cv2.inRange(hsv, ledlower, ledupper)
  maskled = cv2.morphologyEx(maskled,cv2.MORPH_OPEN,kern2)
  maskled = cv2.morphologyEx(maskled,cv2.MORPH_CLOSE,kern2)
  out2.write(maskled)
  c,x=cv2.findContours(maskled,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  ccount = 1
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
        #print("led "+str(ledc)+"on")#DEBUGOFF
#    if(ccount > 5):
#      print("NOISE:")#DEBUG
#      print([xf,yf])
#      break
    if(ledc==-1):	#new led
      ledoff.append(False)
      ledc = len(ledlocs)
      ledlocs.append([xf,yf])
      t.append(time.time())
      print("led "+str(ledc)+" started at loc "+str(xf)+","+str(yf))#DEBUG
    if(time.time() - t[ledc] > .25*(2*ledbit[ledc]+3)):
      ledseq[ledc] = ledseq[ledc]+(128>>ledbit[ledc])
      print("bit "+str(7-ledbit[ledc])+" on led "+str(ledc)+" HIGH")#DEBUG
      print("seq "+str(ledseq[ledc])+" on led "+str(ledc))#DEBUG
      ledbit[ledc] = ledbit[ledc] + 1
    ledoff[ledc] = False
    ccount = ccount + 1
  for c in range(len(ledoff)):
    if(ledoff[c] and ledbit[c]<8):
      #print("led "+str(c)+" off")#DEBUGOFF
      if(time.time() - t[c] > .25*(2*ledbit[c]+3)):
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
      locs[name] = ledlocs[i]
      bluloc[name] = ledlocs[i]
      blkloc[name] = ledlocs[i]
      print("led "+str(i)+" matches seq of "+name)
      break
  c = c + 1

while(1):
  ret, frame = capture.read()
  frame = cv2.warpPerspective(frame,M,(640,480))
  out.write(frame)
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

  redupper = np.array([redmaxh,redmaxs,redmaxv], dtype=np.uint8)
  redlower = np.array([redminh,redmins,redminv], dtype=np.uint8)
  maskred = cv2.inRange(hsv, redlower, redupper)
  maskred = cv2.morphologyEx(maskred,cv2.MORPH_CLOSE,kern16)
  bluupper = np.array([blumaxh,blumaxs,blumaxv], dtype=np.uint8)
  blulower = np.array([bluminh,blumins,bluminv], dtype=np.uint8)
  maskblu = cv2.inRange(hsv, blulower, bluupper)
  maskblu = cv2.morphologyEx(maskblu,cv2.MORPH_OPEN,kern2)
  blkupper = np.array([blkmaxh,blkmaxs,blkmaxv], dtype=np.uint8)
  blklower = np.array([blkminh,blkmins,blkminv], dtype=np.uint8)
  maskblk = cv2.inRange(hsv, blklower, blkupper)
  maskblk = cv2.morphologyEx(maskblk,cv2.MORPH_OPEN,kern2)
  cv2.imshow('maskred',maskred)
  c,x=cv2.findContours(maskred,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  cblu,x=cv2.findContours(maskblu,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  cblk,x=cv2.findContours(maskblk,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
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
    locs[rName]=[xf,yf]

  for i in cblu:
    xf = sum(i[:,0,0])/len(i[:,0,0])
    yf = sum(i[:,0,1])/len(i[:,0,1])
    rName = '?'
    for name in bluloc:
      if(bluloc[name][0]-xf < 20 and bluloc[name][1]-yf < 20):
        rName = name
    if(rName == '?'):
      continue
    bluloc[rName]=[xf,yf]

  for i in cblk:
    xf = sum(i[:,0,0])/len(i[:,0,0])
    yf = sum(i[:,0,1])/len(i[:,0,1])
    rName = '?'
    for name in blkloc:
      if(blkloc[name][0]-xf < 20 and blkloc[name][1]-yf < 20):
        rName = name
    if(rName == '?'):
      continue
    blkloc[rName]=[xf,yf]

  if(count%10 == 0):
    for soc in csoc:
      locxy = locs[soc]
      locxy[0] = int(locxy[0])
      locxy[1] = int(locxy[1])
      strx = str(locxy[0])
      stry = str(locxy[1])
      while(len(strx)<3):#no longer necessary
        strx = "0"+strx	 #
      while(len(stry)<3):#
        stry = "0"+stry  #

      dx = bluloc[soc][0] - blkloc[soc][0]
      dy = bluloc[soc][1] - blkloc[soc][1]
      theta = -(math.atan2(-dy,dx)*180/math.pi - 90)
      if(theta<0):
        theta = theta + 360
      angle = str(int(theta))

      csoc[soc].send((strx+","+stry+":"+angle+" ").encode())

  frame = cv2.resize(frame, (0,0), fx=2, fy=2)
  cv2.imshow('frame', frame)
  k = cv2.waitKey(5) & 0xFF
  count = count + 1
  if k == 27:
    break

cv2.destroyAllWindows()
