import time
from ctypes import *
import cv2.cv as cv
import cv2
import numpy as np

cv.NamedWindow("name", cv.CV_WINDOW_AUTOSIZE)
capture  = cv2.VideoCapture()
capture.open(0)

newx = 320
newy = 240

nx = 640
ny = 480

while True:#Dr. Lofaro's code for getting video feed to a matrix var
  img = np.zeros((newx,newy,3), np.uint8)
  ret, img = capture.read()

  height, width = img.shape[:2]
  hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
  minh,mins,minv = np.amin(np.amin(hsv[78:82,171:175],axis=0),axis=0)
  maxh,maxs,maxv = np.amax(np.amax(hsv[78:82,171:175],axis=0),axis=0)
  print("mins")
  print(minh,mins,minv)
  print("maxs")
  print(maxh,maxs,maxv)
  lower_white = np.array([minh, mins, minv], dtype=np.uint8)
  upper_white = np.array([maxh, maxs, maxv], dtype=np.uint8)
  print(lower_white)
  print(upper_white)
  mask = cv2.inRange(hsv, lower_white, upper_white)
  cv2.imshow("mask", mask)
  img2 = img.copy()
  r,g,b = cv2.split(img2)
  r = r & mask
  g = g & mask
  b = b & mask
  img2 = cv2.merge([r,g,b],img2)
  minh,mins,minv = np.amin(np.amin(img[171:175,78:82],axis=0),axis=0)
  maxh,maxs,maxv = np.amax(np.amax(img[171:175,78:82],axis=0),axis=0)
#  print("img mins")
#  print(minh,mins,minv)
#  print("img maxs")
#  print(maxh,maxs,maxv)
  mom = cv2.moments(mask, True)
  if(mom['m00']!=0):
    xf = int(mom['m10']/mom['m00'])
    yf = int(mom['m01']/mom['m00'])
    cv2.circle(img,(78,171), 1, (255,0,255),-1)
    cv2.circle(img,(82,171), 1, (255,0,255),-1)
    cv2.circle(img,(78,175), 1, (255,0,255),-1)
    cv2.circle(img,(82,175), 1, (255,0,255),-1)
    cv2.circle(mask,(78,171), 1, (255,0,255),-1)
    cv2.circle(mask,(82,171), 1, (255,0,255),-1)
    cv2.circle(mask,(78,175), 1, (255,0,255),-1)
    cv2.circle(mask,(82,175), 1, (255,0,255),-1)
#    cv2.circle(img,(50,140), 1, (255,0,255),-1)
#    cv2.circle(img,(70,140), 1, (255,0,255),-1)
#    cv2.circle(img,(50,160), 1, (255,0,255),-1)
#    cv2.circle(img,(70,160), 1, (255,0,255),-1)
    cv2.circle(img,(xf,yf), 5, (255,50,255),-1)
    print(xf,yf)
  cv2.imshow("name", img)
  cv2.imshow("img2", img2)
  cv2.waitKey(10)
