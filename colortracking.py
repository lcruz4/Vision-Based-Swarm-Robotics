import cv2
import numpy as np
import sys

capture = cv2.VideoCapture()
capture.open(0)
#print(capture.get(int(sys.argv[1])))
#print('MSEC', capture.get(0))
#print('FRAMES', capture.get(1))
#print('RATIO', capture.get(2))
#print('WIDTH', capture.get(3))
#print('HEIGHT', capture.get(4))
#print('FPS', capture.get(5))
#print('FOURCC', capture.get(6))
#print('FRAMECOUNT', capture.get(7))
#print('FORMAT', capture.get(8))
#print('MODE', capture.get(9))
capture.set(int(sys.argv[1]), float(sys.argv[2]))
print('10:BRIGHT', capture.get(10))
print('11:CONTRAST', capture.get(11))
print('12:SATURATION', capture.get(12))
print('13:HUE', capture.get(13))
print('14:GAIN', capture.get(14))
print('15:EXPOSURE', capture.get(15))


nx = 640
ny = 480

kernel = np.ones((1,1),np.uint8)

while(1):
    #frame = np.zeros((nx,ny,3), np.uint8)
    ret, frame = capture.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#    106 63, 225 175
    upper_white = np.array([54,125,255], dtype=np.uint8)
    lower_white = np.array([46,25,150], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_white, upper_white)
    #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    #mask = cv2.dilate(mask, kernel)
    mom = cv2.moments(mask, True)
    if(mom['m00']==0):
      xf = 0
      yf = 0
    else:
      xf = int(mom['m10']/mom['m00'])
      yf = int(mom['m01']/mom['m00'])
      #print(hsv[yf,xf])
    cv2.circle(frame, (xf-2,yf-2), 1, (255,0,255), -1)
    cv2.circle(frame, (xf+2,yf-2), 1, (255,0,255), -1)
    cv2.circle(frame, (xf-2,yf+2), 1, (255,0,255), -1)
    cv2.circle(frame, (xf+2,yf+2), 1, (255,0,255), -1)
    cv2.circle(frame, (145,155), 1, (255,0,255), -1)
    cv2.circle(frame, (155,155), 1, (255,0,255), -1)
    cv2.circle(frame, (145,165), 1, (255,0,255), -1)
    cv2.circle(frame, (155,165), 1, (255,0,255), -1)
    cv2.circle(mask, (145,155), 1, (255,0,255), -1)
    cv2.circle(mask, (155,155), 1, (255,0,255), -1)
    cv2.circle(mask, (145,165), 1, (255,0,255), -1)
    cv2.circle(mask, (155,165), 1, (255,0,255), -1)
    cv2.namedWindow('frame', 0)
    cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
