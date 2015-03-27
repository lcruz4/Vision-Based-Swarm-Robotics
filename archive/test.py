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
        mom = cv2.moments(mask, True)
#        print(mom['m00'],mom['m01'],mom['m02'],mom['m03'])
#        print(mom['m10'],mom['m11'],mom['m12'])
#        print(mom['m20'],mom['m21'])
#        print(mom['m30'])
        xf = int(mom['m20']/mom['m00'])
        yf = int(mom['m02']/mom['m00'])
        cv2.circle(frame, (xf,yf), 1, (255,0,255), -1)
        cv2.rectangle(frame, (lx,ly), (ux,uy), (0,255,0), 0, 8)
        cv2.rectangle(mask, (lx,ly), (ux,uy), (255,255,255), 0, 8)
    else:
        cv2.circle(frame, (xf,yf), 5, (255,0,255), -1)
        cv2.circle(frame, (lx, ly), 1, (0,255,0), -1)
    cv2.imshow("img",frame)
    cv2.imshow("mask",mask)
    time.sleep(1)
#    print("mins")
#    print(minh,mins,minv)
#    print("maxs")
#    print(maxh,maxs,maxv)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
