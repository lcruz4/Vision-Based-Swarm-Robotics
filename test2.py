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
lx,ly,ux,uy = [100,100,110,110]
click = False
t = time.time()
freq = 999999999999999999

f1 = open('mins', 'w')
f2 = open('maxs', 'w')
f3 = open('time', 'w')
f3.write('i	time	frequency\n')
counter = 0
kern4 = np.ones((4,4),np.uint8)
while(1):
    tdiff = time.time()-t
    t = time.time()
    if(tdiff!=0):
      freq = 1/tdiff
    counter = counter + 1
    frame = np.zeros((320,240,3), np.uint8)
    ret, frame = capture.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if(not click):
        minh,mins,minv = np.amin(np.amin(hsv[ly:uy,lx:ux],axis=0),axis=0)
        maxh,maxs,maxv = np.amax(np.amax(hsv[ly:uy,lx:ux],axis=0),axis=0)
        lower_thresh = np.array([minh,mins,minv], dtype=np.uint8)
        upper_thresh = np.array([maxh,maxs,maxv], dtype=np.uint8)
        f1.seek(0)
        f2.seek(0)
        f1.write(str(minh)+'\n'+str(mins)+'\n'+str(minv)+'\n')
        f2.write(str(maxh)+'\n'+str(maxs)+'\n'+str(maxv)+'\n')
	f3.write(str(counter)+':	'+str(tdiff)+
                 '	'+str(freq)+'\n')
        mask = cv2.inRange(hsv, lower_thresh, upper_thresh)
        mask1 = cv2.inRange(hsv, lower_thresh, upper_thresh)
        #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kern4)
        
        cv2.rectangle(mask1, (lx,ly), (ux,uy), (255,255,255), 0, 8)
        cv2.imshow("mask1",mask1)
        con, hie = cv2.findContours(mask,1,2)
        M = cv2.moments(con[0])
        if(M['m00']!=0):
          cx = int(M['m10']/M['m00'])
          cy = int(M['m01']/M['m00'])
          cv2.circle(frame, (cx,cy), 1, (255,0,255), -1)
        cv2.rectangle(frame, (lx,ly), (ux,uy), (0,255,0), 0, 8)
    cv2.rectangle(frame, (c,r), (c+w,r+h), 255,2)
    cv2.imshow("img",frame)
    cv2.imshow("mask",mask)
#    print("mins")
#    print(minh,mins,minv)
#    print("maxs")
#    print(maxh,maxs,maxv)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
