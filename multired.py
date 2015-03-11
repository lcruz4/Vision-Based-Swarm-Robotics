import cv2
import numpy as np

kernel = np.ones((15,15),np.uint8)

while(1):
  img = cv2.imread('img.png', CV_LOAD_IMAGE_COLOR)
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

  minh = 48
  mins = 32
  minv = 130
  maxh = 83
  maxs = 107
  maxv = 213
  upper_red = np.array([maxh,maxs,maxv], dtype=np.uint8)
  lower_red = np.array([minh,mins,minv], dtype=np.uint8)
  maskred = cv2.inRange(hsv, lower_red, upper_red)
  maskred = cv2.morphologyEx(maskred,cv2.MORPH_CLOSE,kernel)
  maskblu = cv2.inRange(hsv, lower_blu, upper_blu)
  cv2.imshow('maskred',maskred)
  c,x=cv2.findContours(maskred,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
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
