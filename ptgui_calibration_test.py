import cv2
import json
import numpy as np

import matplotlib.pyplot as plt

# INPUTS
imgL = cv2.imread("calibration_files/left_checkerboard.png")
imgR = cv2.imread("calibration_files/right_checkerboard.png")

chessboard_dims = (12,12)

# STEP 0: LOAD CHESSBOARD POINTS FROM PTGUI ---------------------------------------------------------
with open("calibration_files/calibrationfile12x12.pts") as f:
  ptgui_dict = json.load(f)

raw_points = ptgui_dict["project"]["controlpoints"]

cornersL = []
cornersR = []
for pt in raw_points:
    l_pt = np.array([pt['0'][2:]], np.float32)
    r_pt = np.array([pt['1'][2:]], np.float32)
    cornersL.append(l_pt)
    cornersR.append(r_pt)

cornersL = np.array(cornersL, np.float32)
cornersR = np.array(cornersR, np.float32)

# STEP 1: CALIBRATE CAMERAS ---------------------------------------------------------
imgL_gray = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
imgR_gray = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

objp = np.zeros((1, chessboard_dims[0]*chessboard_dims[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:chessboard_dims[0],0:chessboard_dims[1]].T.reshape(-1, 2)

K_L, K_R = np.zeros((3, 3)), np.zeros((3, 3))
D_L, D_R = np.zeros((4, 1)), np.zeros((4, 1))

img_ptsL = [cornersL]
img_ptsR = [cornersR]
obj_pts = [objp]

retL, mtxL, distL, rvecsL, tvecsL = \
    cv2.fisheye.calibrate(obj_pts, img_ptsL, imgL_gray.shape[::-1], K_L, D_L)

retR, mtxR, distR, rvecsR, tvecsR = \
    cv2.fisheye.calibrate(obj_pts, img_ptsR, imgR_gray.shape[::-1], K_R, D_R)

map1L, map2L = cv2.fisheye.initUndistortRectifyMap(K_L, D_L, np.eye(3), K_L, imgL_gray.shape[::-1], cv2.CV_16SC2)
undistorted_imgL = cv2.remap(imgL, map1L, map2L, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

map1R, map2R = cv2.fisheye.initUndistortRectifyMap(K_R, D_R, np.eye(3), K_R, imgR_gray.shape[::-1], cv2.CV_16SC2)
undistorted_imgR = cv2.remap(imgR, map1R, map2R, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

print(K_L)
print(K_R)
print(D_L)
print(D_R)
cv2.namedWindow("Left image before rectification", cv2.WINDOW_NORMAL)
cv2.namedWindow("Right image before rectification", cv2.WINDOW_NORMAL)
cv2.drawChessboardCorners(imgL, chessboard_dims, cornersL, True)
cv2.drawChessboardCorners(imgR, chessboard_dims, cornersR, True)
cv2.imshow("Left image before rectification", imgL)
cv2.imshow("Right image before rectification", imgR)

cv2.namedWindow("Left image after rectification", cv2.WINDOW_NORMAL)
cv2.namedWindow("Right image after rectification", cv2.WINDOW_NORMAL)
cv2.imshow("Left image after rectification", undistorted_imgL)
cv2.imshow("Right image after rectification", undistorted_imgR)

cv2.waitKey(0)
