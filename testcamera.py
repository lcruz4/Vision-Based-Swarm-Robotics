import cv2

capture = cv2.VideoCapture()
capture.open(0)

while(1):
    ret, frame = capture.read()
    cv2.imshow('frame',frame)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
