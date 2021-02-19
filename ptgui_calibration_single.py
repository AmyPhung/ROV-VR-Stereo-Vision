import cv2
import json
import numpy as np

import matplotlib.pyplot as plt

# INPUTS
imgL = cv2.imread("calibration_files/left_checkerboard.png")

chessboard_dims = (15,12)

# STEP 0: LOAD CHESSBOARD POINTS FROM PTGUI ---------------------------------------------------------
with open("calibration_files/calibrationfile_full_board.pts") as f:
  ptgui_dict = json.load(f)

raw_points = ptgui_dict["project"]["controlpoints"]

cornersL = []
for pt in raw_points:
    l_pt = np.array([pt['0'][2:]], np.float32)
    cornersL.append(l_pt)

print("raw_points size: ", len(raw_points))

cornersL = np.array(cornersL, np.float32)
print("cornersL size: ", len(cornersL))

# STEP 1: CALIBRATE CAMERAS ---------------------------------------------------------
imgL_gray = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)

objp = np.zeros((1, chessboard_dims[0]*chessboard_dims[1], 3), np.float32)
print("objp\n", objp.shape)

objp[0,:,:2] = np.mgrid[0:chessboard_dims[0],0:chessboard_dims[1]].T.reshape(-1, 2)
# print(objp[0,:,:2])

K_L = np.zeros((3, 3))
D_L = np.zeros((4, 1))

img_ptsL = [cornersL]
obj_pts = [objp]

print("img_ptsL info:")
print(img_ptsL[0].shape)
print(img_ptsL[0][:,:,:].T)

# obj_pts contains a meshgrid covering the whole area of the chessboard and
# this gives the coordinates of each vertex on the chessboard (where it should be
# were the image not warped)

# img_ptsL contains the x,y coordinates of all the chessboard points that were
# marked in the calibration file

cv2.fisheye.calibrate(obj_pts, img_ptsL, imgL_gray.shape[::-1], K_L, D_L)
# print("K_L\n",K_L)
"""
nk = k.copy()
nk[0,0]=k[0,0]/2
nk[1,1]=k[1,1]/2
# Just by scaling the matrix coefficients!

map1, map2 = cv2.fisheye.initUndistortRectifyMap(k, d, np.eye(3), nk, (800,600), cv2.CV_16SC2)  # Pass k in 1st parameter, nk in 4th parameter
nemImg = cv2.remap( img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
"""

nK_L = K_L.copy()
# nK_L[0,0] = K_L[0,0]*0.8
# nK_L[1,1] = K_L[1,1]*0.8

# Single-camera rectification
map1L, map2L = cv2.fisheye.initUndistortRectifyMap(K_L, D_L, np.eye(3), nK_L, imgL_gray.shape[::-1], cv2.CV_16SC2)
undistorted_imgL = cv2.remap(imgL, map1L, map2L, interpolation=cv2.INTER_LINEAR)#, borderMode=cv2.BORDER_CONSTANT)

cv2.namedWindow("Left image after rectification", cv2.WINDOW_NORMAL)
cv2.imshow("Left image after rectification", undistorted_imgL)

cv2.waitKey(0)
