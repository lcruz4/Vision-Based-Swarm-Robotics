import cv2
import numpy as np

kern1 = np.ones((1,1),np.uint8)
kern2 = np.ones((2,2),np.uint8)
kern4 = np.ones((4,4),np.uint8)
kern8 = np.ones((8,8),np.uint8)
cv2.namedWindow('frame', 0)
capture = cv2.VideoCapture()
capture.open(0)

while(1):
  ret, frame = capture.read()
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

  redmax = open('./Maxs/maxs','r')
  redmin = open('./Maxs/mins','r')
  maxh = redmax.readline()
  maxs = redmax.readline()
  maxv = redmax.readline()
  minh = redmin.readline()
  mins = redmin.readline()
  minv = redmin.readline()
  redmax.close()
  redmin.close()

  upper_red = np.array([maxh,maxs,maxv], dtype=np.uint8)
  lower_red = np.array([minh,mins,minv], dtype=np.uint8)
  maskred = cv2.inRange(hsv, lower_red, upper_red)
  maskred = cv2.morphologyEx(maskred,cv2.MORPH_CLOSE,kern8)
  cv2.imshow('maskred',maskred)
  c,x=cv2.findContours(maskred,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  for i in c:
    xf = sum(i[:,0,0])/len(i[:,0,0])
    yf = sum(i[:,0,1])/len(i[:,0,1])
    cv2.circle(frame, (xf,yf), 2, (0,255,0), -1)

  frame = cv2.resize(frame, (0,0), fx=2, fy=2)
  cv2.imshow('frame', frame)
  k = cv2.waitKey(5) & 0xFF
  if k == 27:
    break

cv2.destroyAllWindows()
