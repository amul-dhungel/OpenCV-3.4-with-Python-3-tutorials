from webbrowser import open_new
import cv2
import numpy as np


def nothing(x):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H","Trackbars",0,179,nothing)
cv2.createTrackbar("L - S","Trackbars",0,255,nothing)
cv2.createTrackbar("L - V","Trackbars",0,255,nothing)
cv2.createTrackbar("U - H","Trackbars",179,179,nothing)
cv2.createTrackbar("U - S","Trackbars",255,255,nothing)
cv2.createTrackbar("U - V","Trackbars",255,255,nothing)



while True:
    _, frame = cap.read()

    # a blue marker , pixel value is not same around
    # due to light, every pixel values are different
    # so for this, you have define a color range, that 
    # stimulates the blue color
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # getting values from trackbar pos
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    lower_blue = np.array([l_h,l_s,l_v])
    upper_blue = np.array([u_h,u_s,u_v])

    # masking the specific color range
    mask = cv2.inRange(hsv,lower_blue,upper_blue)

    # using of noise removing functions 
    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(mask,kernel)
    dilation = cv2.dilate(mask,kernel)

    opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel,iterations=2)
    closing = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)

    # results, it means blending of original image with filter mask image.
    result = cv2.bitwise_and(frame,frame, mask = mask)

    # displaying the video 
    # cv2.imshow("ODetection",frame)
    cv2.imshow("mask",mask)
    cv2.imshow("erosion",erosion)
    cv2.imshow("dilation",dilation)
    cv2.imshow("opening",opening)
    cv2.imshow("closing",closing)
    # cv2.imshow("Final blending", result)


    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()