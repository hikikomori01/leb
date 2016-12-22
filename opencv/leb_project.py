import cv2
import numpy as np
import imutils


def color_seg(choice):
    if choice == 'blue':
        lower_hue = np.array([100])
        upper_hue = np.array([150])
    elif choice == 'white':
        lower_hue = np.array([0])
        upper_hue = np.array([0])
    elif choice == 'black':
        lower_hue = np.array([150])
        upper_hue = np.array([200])
    return lower_hue, upper_hue

def create_graph(vertex, color):
    for g in range(0, len(vertex)-1):
        for y in range(0, len(vertex[0][0])-1):
            cv2.circle(gray, (vertex[g][0][y], vertex[g][0][y+1]), 3, (255,255,255), -1)
            cv2.line(gray, (vertex[g][0][y], vertex[g][0][y+1]), (vertex[g+1][0][y], vertex[g+1][0][y+1]), color, 2)
    cv2.line(gray, (vertex[len(vertex)-1][0][0], vertex[len(vertex)-1][0][1]), (vertex[0][0][0], vertex[0][0][1]), color, 2)



cap = cv2.VideoCapture(0)
while (True):

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)





    chosen_color = 'black'
    lower_hue, upper_hue = color_seg(chosen_color)

    mask = cv2.inRange(gray, lower_hue, upper_hue)
    value = (37, 37)
    blurred = cv2.GaussianBlur(mask, value, 0)

    _, thresh1 = cv2.threshold(blurred, 127, 255,
                               cv2.THRESH_BINARY)
    _, contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # print(contours)
    # cnt = contours[0]
    for b, cnt in enumerate(contours):
        if hierarchy[0, b, 3] == -1:  # <-the mistake might be here
            approx = cv2.approxPolyDP(cnt, 0.001 * cv2.arcLength(cnt, True), True)
            clr = (255, 0, 0)
            create_graph(approx, clr)
            area = cv2.contourArea(cnt)
            print(area)
    print("==================")
    # break
    #
    # epsilon = 0.1 * cv2.arcLength(cnt, True)
    # approx = cv2.approxPolyDP(cnt, epsilon, True)
    #
    # (x, y), radius = cv2.minEnclosingCircle(cnt)
    # center = (int(x), int(y))
    # radius = int(radius)
    # cv2.circle(frame, center, radius, (0, 0, 0), 2)

    cv2.imshow('frame', frame)
    cv2.imshow('gray', gray)
    cv2.imshow('mask', mask)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
