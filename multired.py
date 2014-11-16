import cv2
import numpy as np

img = cv2.imread("img.bmp", cv2.CV_LOAD_IMAGE_COLOR)

upper_thresh = np.array([64,32,224], dtype=np.uint8)
lower_thresh = np.array([64,32,224], dtype=np.uint8)
mask = cv2.inRange(img, lower_thresh, upper_thresh)
c,x=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
for i in c:
  xf = sum(i[:,0,0])/len(i[:,0,0])
  yf = sum(i[:,0,1])/len(i[:,0,1])
  cv2.circle(img, (xf,yf), 2, (0,255,0), -1)

cv2.imshow('img', img)
cv2.waitKey(0)

cv2.destroyAllWindows()
