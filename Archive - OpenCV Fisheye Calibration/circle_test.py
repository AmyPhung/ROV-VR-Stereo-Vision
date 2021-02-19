# import cv2
# import numpy as np
#
# img = cv2.imread('calibration_files/right_checkerboard - Copy.png', cv2.IMREAD_GRAYSCALE)
# img = cv2.medianBlur(img,5)
# cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
# print("1")
# circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,dp=3,minDist=20,
#                             param1=50,param2=30,minRadius=30,maxRadius=0)
# print("2")
# circles = np.uint16(np.around(circles))
# print("3")
#
# for i in circles[0,:]:
#     # draw the outer circle
#     cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
#     # draw the center of the circle
#     cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
# print("4")
# cv2.imshow('detected circles',cimg)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

import cv2

originalImage = cv2.imread('calibration_files/right_checkerboard - Copy.png')
grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)

(thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 20, 255, cv2.THRESH_BINARY)

cv2.imshow('Black white image', blackAndWhiteImage)
cv2.imshow('Original image',originalImage)
cv2.imshow('Gray image', grayImage)

cv2.waitKey(0)
cv2.destroyAllWindows()
