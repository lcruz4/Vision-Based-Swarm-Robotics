import cv2
import numpy as np

capture = cv2.VideoCapture()
capture.open(0)
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))
kernel = np.ones((15,15),np.uint8)

while(1):
  ret, img = capture.read()
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

  minh = 4
  mins = 190
  minv = 110
  maxh = 10
  maxs = 255
  maxv = 173
  upper_thresh = np.array([maxh,maxs,maxv], dtype=np.uint8)
  lower_thresh = np.array([minh,mins,minv], dtype=np.uint8)
  mask = cv2.inRange(hsv, lower_thresh, upper_thresh)
  mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
  cv2.imshow('mask',mask)
  c,x=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  for i in c:
    xf = sum(i[:,0,0])/len(i[:,0,0])
    yf = sum(i[:,0,1])/len(i[:,0,1])
    cv2.circle(img, (xf,yf), 2, (0,255,0), -1)

  img = cv2.resize(img, (0,0), fx=2, fy=2)
  out.write(img)
  cv2.imshow('img', img)
  k = cv2.waitKey(5) & 0xFF
  if k == 27:
    break

cv2.destroyAllWindows()
