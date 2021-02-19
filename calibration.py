import cv2
import numpy as np

Limg = cv2.imread('left_checkerboard.png')
Rimg = cv2.imread('right_checkerboard.png')

width = 700 # Adjust this for speed

Lscale = width/Limg.shape[1]
Rscale = width/Rimg.shape[1]
Lheight = int(Lscale * Limg.shape[0])
Rheight = int(Rscale * Rimg.shape[0])

Ldim = (width, Lheight)
Rdim = (width, Rheight)

# resize image
Lresized = cv2.resize(Limg, Ldim, interpolation = cv2.INTER_AREA)
Rresized = cv2.resize(Rimg, Rdim, interpolation = cv2.INTER_AREA)

cv2.imshow("detected circles", Lresized)

def findCircle(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    rows = gray.shape[0]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=100, param2=100,
                               minRadius=1, maxRadius=10000)
    return circles[0][0]

def displayCircle(img, circle, window_name):
    print(circle)
    center = (circle[0], circle[1])
    # circle center
    cv2.circle(img, center, 1, (0, 100, 100), 3)
    # circle outline
    radius = int(circle[2])
    cv2.circle(img, center, radius, (255, 0, 255), 3)

    cv2.imshow(window_name, img)

Lcircle = findCircle(Lresized)
Rcircle = findCircle(Rresized)

displayCircle(Lresized, Lcircle, "Left Output")
displayCircle(Rresized, Rcircle, "Right Output")


f = open("calibration.txt", "w")
print("Right Center X:", str(Rcircle[0]/width), file=f)
print("Right Center Y:", str(Rcircle[1]/Rheight), file=f)
print("Right Radius X:", str(Rcircle[2]/width), file=f)
print("Right Radius Y:", str(Rcircle[2]/Rheight), file=f)
print("Left Center X:", str(Lcircle[0]/width), file=f)
print("Left Center Y:", str(Lcircle[1]/Lheight), file=f)
print("Left Radius X:", str(Lcircle[2]/width), file=f)
print("Left Radius Y:", str(Lcircle[2]/Lheight), file=f)
f.close()


cv2.waitKey(0)
cv2.destroyAllWindows()
