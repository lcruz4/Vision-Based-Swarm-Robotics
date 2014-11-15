import cv2
import numpy as np

capture = cv2.VideoCapture()
capture.open(0)

newx = 320
newy = 240

nx = 640
ny = 480

while(1):
    frame = np.zeros((newx,newy,3), np.uint8)
    ret, frame = capture.read()
#    frameBGR = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of white color in HSV
    # change it according to your need !
    # blue
    minh,mins,minv = np.amin(np.amin(hsv[155:165,145:155],axis=0),axis=0)
    maxh,maxs,maxv = np.amax(np.amax(hsv[155:165,145:155],axis=0),axis=0)
    upper_white = np.array([maxh,maxs,maxv], dtype=np.uint8)
    lower_white = np.array([minh,mins,minv], dtype=np.uint8)

    # green
#    upper_white = np.array([70,255,255], dtype=np.uint8)
#    lower_white = np.array([50,0,0], dtype=np.uint8)

    # red
#    upper_white = np.array([20,255,255], dtype=np.uint8)
#    lower_white = np.array([0,100,100], dtype=np.uint8)

    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv, lower_white, upper_white)
    # Bitwise-AND mask and original image
    mom = cv2.moments(mask, True)
    xf = int(mom['m10']/mom['m00'])
    yf = int(mom['m01']/mom['m00'])
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
