import cv2
import numpy as np
import sys
import time
def onmouse(event, x, y, flags, param):
    if flags & cv2.EVENT_FLAG_LBUTTON:
        global click, ux, uy, lx, ly
        if click and x>lx and y>ly:
            ux = x
            uy = y
            click = False
        else:
            lx = x
            ly = y
            click = True

cv2.namedWindow("img", 0)
cv2.setMouseCallback("img", onmouse)
r,h,c,w = 100, 100,100,100
track_window = (c,r,w,h)
capture = cv2.VideoCapture()
capture.open(0)
ret, frame = capture.read()
lx,ly,ux,uy = [100,100,110,110]
click = False
t = time.time()
freq = 999999999999999999

roi = frame[r:r+h, c:c+w]
hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
minh,mins,minv = np.amin(np.amin(hsv_roi[ly:uy,lx:ux],axis=0),axis=0)
maxh,maxs,maxv = np.amax(np.amax(hsv_roi[ly:uy,lx:ux],axis=0),axis=0)
lower_thresh = np.array([minh,mins,minv], dtype=np.uint8)
upper_thresh = np.array([maxh,maxs,maxv], dtype=np.uint8)
mask = cv2.inRange(hsv_roi, lower_thresh, upper_thresh)
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

term_crit = (cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,10,1)

f1 = open('./Maxs/mins', 'w')
f2 = open('./Maxs/maxs', 'w')
counter = 0
kern4 = np.ones((4,4),np.uint8)
while(1):
    if(not click):
      roi = frame[r:r+h, c:c+w]
      hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      minh,mins,minv = np.amin(np.amin(hsv_roi[ly:uy,lx:ux],axis=0),axis=0)
      maxh,maxs,maxv = np.amax(np.amax(hsv_roi[ly:uy,lx:ux],axis=0),axis=0)
      lower_thresh = np.array([minh,mins,minv], dtype=np.uint8)
      upper_thresh = np.array([maxh,maxs,maxv], dtype=np.uint8)
      mask = cv2.inRange(hsv_roi, lower_thresh, upper_thresh)
      roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
      cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
      ret, frame = capture.read()
      if(ret == True):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
        ret, track_window = cv2.CamShift(dst,track_window,term_crit)
    pts = cv2.boxPoints(ret)
    pts = np.int0(pts)
    cv2.polylines(frame,[pts],True,255,2)
#    x,y,w,h = track_window
#    cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
    cv2.imshow("img",frame)
    cv2.imshow("mask",mask)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
