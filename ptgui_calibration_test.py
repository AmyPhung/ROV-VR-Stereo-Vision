import cv2
import json
import numpy as np

import matplotlib.pyplot as plt

# INPUTS
imgL = cv2.imread("calibration_files/left_checkerboard.png")
imgR = cv2.imread("calibration_files/right_checkerboard.png")

chessboard_dims = (15,12)

# STEP 0: LOAD CHESSBOARD POINTS FROM PTGUI ---------------------------------------------------------
with open("calibration_files/calibrationfile_full_board.pts") as f:
  ptgui_dict = json.load(f)

raw_points = ptgui_dict["project"]["controlpoints"]

cornersL = []
cornersR = []
for pt in raw_points:
    l_pt = np.array([pt['0'][2:]], np.float32)
    r_pt = np.array([pt['1'][2:]], np.float32)
    cornersL.append(l_pt)
    cornersR.append(r_pt)

print("raw_points size: ", len(raw_points))

cornersL = np.array(cornersL, np.float32)
cornersR = np.array(cornersR, np.float32)
print("cornersL size: ", len(cornersL))

# STEP 1: CALIBRATE CAMERAS ---------------------------------------------------------
imgL_gray = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
imgR_gray = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

objp = np.zeros((1, chessboard_dims[0]*chessboard_dims[1], 3), np.float32)
print("objp\n", objp.shape)

objp[0,:,:2] = np.mgrid[0:chessboard_dims[0],0:chessboard_dims[1]].T.reshape(-1, 2)
# print(objp[0,:,:2])

K_L, K_R = np.zeros((3, 3)), np.zeros((3, 3))
D_L, D_R = np.zeros((4, 1)), np.zeros((4, 1))

img_ptsL = [cornersL]
img_ptsR = [cornersR]
obj_pts = [objp]

print("img_ptsL info:")
print(img_ptsL[0].shape)
print(img_ptsL[0][:,:,:].T)

# obj_pts contains a meshgrid covering the whole area of the chessboard and
# this gives the coordinates of each vertex on the chessboard (where it should be
# were the image not warped)

# img_ptsL contains the x,y coordinates of all the chessboard points that were
# marked in the calibration file 

retL, mtxL, distL, rvecsL, tvecsL = \
    cv2.fisheye.calibrate(obj_pts, img_ptsL, imgL_gray.shape[::-1], K_L, D_L)
# print("K_L\n",K_L)

retR, mtxR, distR, rvecsR, tvecsR = \
    cv2.fisheye.calibrate(obj_pts, img_ptsR, imgR_gray.shape[::-1], K_R, D_R)


# STEP 2: Calibrate stereo pair -------------------------------------------------
flags = 0
flags |= cv2.CALIB_FIX_INTRINSIC
# Here we fix the intrinsic camara matrixes so that only Rot, Trns, Emat and Fmat are calculated.
# Hence intrinsic parameters are the same
criteria_stereo= (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# This step is performed to transformation between the two cameras and calculate Essential and Fundamenatl matrix
retS, new_mtxL, distL, new_mtxR, distR, Rot, Trns, Emat, Fmat = \
    cv2.stereoCalibrate(obj_pts, img_ptsL, img_ptsR, mtxL, distL, mtxR, distR,
                        imgL_gray.shape[::-1], criteria_stereo, flags)


# https://learnopencv.com/making-a-low-cost-stereo-camera-using-opencv/
#### STEP 3: Stereo Rectification #######################################
# Using the camera intrinsics and the rotation and translation between
# the cameras, we can now apply stereo rectification. Stereo
# rectification applies rotations to make both camera image planes be
# in the same plane. Along with the rotation matrices, the
# stereoRectify method also returns the projection matrices in the new
# coordinate space.

rectify_scale= 1
rect_l, rect_r, proj_mat_l, proj_mat_r, Q, roiL, roiR = \
    cv2.stereoRectify(new_mtxL, distL, new_mtxR, distR,
                      imgL_gray.shape[::-1], Rot, Trns, rectify_scale, (0,0))
"""
TODO: Save these parameters
"""

#### STEP 4: ###########################################################
#  Compute the mapping required to obtain the undistorted rectified stereo image pair
Left_Stereo_Map= cv2.initUndistortRectifyMap(new_mtxL, distL, rect_l, proj_mat_l,
                                             imgL_gray.shape[::-1], cv2.CV_16SC2)
Right_Stereo_Map= cv2.initUndistortRectifyMap(new_mtxR, distR, rect_r, proj_mat_r,
                                              imgR_gray.shape[::-1], cv2.CV_16SC2)

# print(Left_Stereo_Map)
# print(Right_Stereo_Map)

#### STEP 5: Create 3D Frame ###########################################
Left_nice = cv2.remap(imgL,Left_Stereo_Map[0],Left_Stereo_Map[1],
                      cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
Right_nice = cv2.remap(imgR,Right_Stereo_Map[0],Right_Stereo_Map[1],
                       cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

cv2.namedWindow("Left image before rectification", cv2.WINDOW_NORMAL)
cv2.namedWindow("Right image before rectification", cv2.WINDOW_NORMAL)
cv2.drawChessboardCorners(imgL, chessboard_dims, cornersL, True)
cv2.drawChessboardCorners(imgR, chessboard_dims, cornersR, True)
cv2.imshow("Left image before rectification", imgL)
cv2.imshow("Right image before rectification", imgR)

# Single-camera rectification
map1L, map2L = cv2.fisheye.initUndistortRectifyMap(K_L, D_L, np.eye(3), K_L, imgL_gray.shape[::-1], cv2.CV_16SC2)
undistorted_imgL = cv2.remap(imgL, map1L, map2L, interpolation=cv2.INTER_LINEAR)#, borderMode=cv2.BORDER_CONSTANT)

map1R, map2R = cv2.fisheye.initUndistortRectifyMap(K_R, D_R, np.eye(3), K_R, imgR_gray.shape[::-1], cv2.CV_16SC2)
undistorted_imgR = cv2.remap(imgR, map1R, map2R, interpolation=cv2.INTER_LINEAR)#, borderMode=cv2.BORDER_CONSTANT)

cv2.namedWindow("Left image after rectification", cv2.WINDOW_NORMAL)
cv2.namedWindow("Right image after rectification", cv2.WINDOW_NORMAL)
cv2.imshow("Left image after rectification", undistorted_imgL)
cv2.imshow("Right image after rectification", undistorted_imgR)

# Stereo rectification
cv2.namedWindow("Left image after stereo rectification", cv2.WINDOW_NORMAL)
cv2.namedWindow("Right image after stereo rectification", cv2.WINDOW_NORMAL)
cv2.imshow("Left image after stereo rectification", Left_nice)
cv2.imshow("Right image after stereo rectification", Right_nice)

cv2.waitKey(0)
