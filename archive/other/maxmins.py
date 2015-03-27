import cv2
import numpy as np

capture = cv2.VideoCapture()
capture.open(0)

newx = 320
newy = 240

nx = 640
ny = 480

f1 = open('mins', 'w')
f2 = open('maxs', 'w')
while(1):
    frame = np.zeros((newx,newy,3), np.uint8)
    ret, frame = capture.read()
#    frameBGR = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    minh,mins,minv = np.amin(np.amin(hsv[195:200,125:130],axis=0),axis=0)
    maxh,maxs,maxv = np.amax(np.amax(hsv[195:200,125:130],axis=0),axis=0)
    upper_white = np.array([maxh,maxs,maxv], dtype=np.uint8)
    lower_white = np.array([minh,mins,minv], dtype=np.uint8)
    f1.write(str(minh)+','+str(mins)+','+str(minv)+'\n')
    f2.write(str(maxh)+','+str(maxs)+','+str(maxv)+'\n')
    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv, lower_white, upper_white)
    # Bitwise-AND mask and original image
    mom = cv2.moments(mask, True)
    xf = int(mom['m10']/mom['m00'])
    yf = int(mom['m01']/mom['m00'])
    cv2.circle(frame, (xf,yf), 5, (255,0,255), -1)
    cv2.circle(frame, (125,195), 1, (255,0,255), -1)
    cv2.circle(frame, (130,195), 1, (255,0,255), -1)
    cv2.circle(frame, (125,200), 1, (255,0,255), -1)
    cv2.circle(frame, (130,200), 1, (255,0,255), -1)
    cv2.circle(mask, (125,195), 1, (255,0,255), -1)
    cv2.circle(mask, (130,195), 1, (255,0,255), -1)
    cv2.circle(mask, (125,200), 1, (255,0,255), -1)
    cv2.circle(mask, (130,200), 1, (255,0,255), -1)
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    print(xf, yf)
#    print("mins")
#    print(minh,mins,minv)
#    print("maxs")
#    print(maxh,maxs,maxv)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
