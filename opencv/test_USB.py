import cv2
import numpy as np

def create_graph(vertex, color):
    for g in range(0, len(vertex)-1):
        for y in range(0, len(vertex[0][0])-1):
            cv2.circle(img2gray, (vertex[g][0][y], vertex[g][0][y+1]), 3, (255,255,255), -1)
            cv2.line(img2gray, (vertex[g][0][y], vertex[g][0][y+1]), (vertex[g+1][0][y], vertex[g+1][0][y+1]), color, 2)
    cv2.line(img2gray, (vertex[len(vertex)-1][0][0], vertex[len(vertex)-1][0][1]), (vertex[0][0][0], vertex[0][0][1]), color, 2)

# img1 = cv2.imread('d.jpg')
img2 = cv2.imread('size.png')

 # I want to put logo on top-left corner, So I create a ROI

rows, cols, channels = img2.shape
# roi = img1[0:rows, 0:cols]

 # Now create a mask of logo and create its inverse mask also
img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)

ma = cv2.inRange(mask, 0, 255)

value = (37, 37)
blurred = cv2.GaussianBlur(ma, value, 0)

_, thresh1 = cv2.threshold(blurred, 127, 255,
                           cv2.THRESH_BINARY)
_, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # W-B fream simple

for b, cnt in enumerate(contours):
    if hierarchy[0, b, 3] == -1:  # <-the mistake might be here
        approx = cv2.approxPolyDP(cnt, 0.001 * cv2.arcLength(cnt, True), True)
        clr = (255, 0, 0)
        create_graph(approx, clr)
        area = cv2.contourArea(cnt)
        print(area)

cv2.imshow('res', img2gray)
cv2.waitKey(0)
cv2.destroyAllWindows()