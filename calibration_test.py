
"""
Notes

findChessboardCorners
ret = true/false, whether it's successful
corners = [[[1423 235352]]
           [[1423 235352]]
           [[1423 235352]]
           [[1423 235352]]]
Ordered from left to right, then top to bottom (in a zig zag)
"""

import cv2
import numpy as np

import matplotlib.pyplot as plt

# INPUTS
imgL = cv2.imread("test_footage/image-001.jpg")
imgR = cv2.imread("test_footage/image-011.jpg")

chessboard_dims = (9,6) # inner corners only

# STEP 1: CALIBRATE CAMERAS ---------------------------------------------------------
img_ptsL = []
img_ptsR = []
obj_pts = []

# Create checkerboard reference points in one long list
# (0,0), (1,0), (2,0), ...
# (0,1), (1,1), (2,1), ...
# (0,2), (1,2), (2,2), ...
# ...  , ...  , ...  , ...
objp = np.zeros((chessboard_dims[0]*chessboard_dims[1],3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

# Find corners in all calibration images
for i in range(1):
    imgL_gray = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
    imgR_gray = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    retL, cornersL = cv2.findChessboardCorners(imgL_gray,chessboard_dims,cv2.CALIB_CB_ADAPTIVE_THRESH+cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)
    retR, cornersR =  cv2.findChessboardCorners(imgR_gray,chessboard_dims,cv2.CALIB_CB_ADAPTIVE_THRESH+cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)

    # Note: these corners need to be in order of left to right, then top to bottom in a zig zag - this is important for camera calibration

    # If we successfully found corners
    if retL and retR:
        img_ptsL.append(cornersL)
        img_ptsR.append(cornersR)
        obj_pts.append(objp)

    # Note: we can use more than one image in calibrate camera, we just need to extend obj_pts and cornersL

# Calibrating left camera
retL, mtxL, distL, rvecsL, tvecsL = cv2.calibrateCamera(obj_pts,img_ptsL,imgL_gray.shape[::-1],None,None)
hL,wL= imgL_gray.shape[:2]
new_mtxL, roiL= cv2.getOptimalNewCameraMatrix(mtxL,distL,(wL,hL),1,(wL,hL))

# Calibrating right camera
retR, mtxR, distR, rvecsR, tvecsR = cv2.calibrateCamera(obj_pts,img_ptsR,imgR_gray.shape[::-1],None,None)
hR,wR= imgR_gray.shape[:2]
new_mtxR, roiR= cv2.getOptimalNewCameraMatrix(mtxR,distR,(wR,hR),1,(wR,hR))

"""
Sample output:
print(new_mtxL)
print(roiL)
print(new_mtxR)
print(roiR)

print(distL)
print(distR)

[[1.98021606e+03 0.00000000e+00 5.08686844e+02]
 [0.00000000e+00 1.35376221e+03 4.48122927e+02]
 [0.00000000e+00 0.00000000e+00 1.00000000e+00]]
(461, 424, 290, 43)
[[8.82812927e+02 0.00000000e+00 5.15340160e+02]
 [0.00000000e+00 1.50557703e+03 4.06838657e+02]
 [0.00000000e+00 0.00000000e+00 1.00000000e+00]]
(6, 78, 1258, 656)

[[-4.84956550e+00 -4.76655987e+01  7.19306849e-02 -2.42038917e-01
   1.13891549e+03]]
[[ 1.90098445 -3.9679683  -0.02126505 -0.05786807  2.60594189]]
"""

# STEP 2: Calibrate stereo pair -------------------------------------------------
"""
Requirements:
- checkerboard corners
- checkerboard corner index
- camera intrinsic matrices
- dist
"""
flags = 0
flags |= cv2.CALIB_FIX_INTRINSIC
# Here we fix the intrinsic camara matrixes so that only Rot, Trns, Emat and Fmat are calculated.
# Hence intrinsic parameters are the same
criteria_stereo= (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# This step is performed to transformation between the two cameras and calculate Essential and Fundamenatl matrix
retS, new_mtxL, distL, new_mtxR, distR, Rot, Trns, Emat, Fmat = cv2.stereoCalibrate(obj_pts, img_ptsL, img_ptsR, new_mtxL, distL, new_mtxR, distR, imgL_gray.shape[::-1], criteria_stereo, flags)



# https://learnopencv.com/making-a-low-cost-stereo-camera-using-opencv/
#### STEP 3: Stereo Rectification #######################################
# Using the camera intrinsics and the rotation and translation between
# the cameras, we can now apply stereo rectification. Stereo
# rectification applies rotations to make both camera image planes be
# in the same plane. Along with the rotation matrices, the
# stereoRectify method also returns the projection matrices in the new
# coordinate space.

rectify_scale= 1
rect_l, rect_r, proj_mat_l, proj_mat_r, Q, roiL, roiR= cv2.stereoRectify(new_mtxL, distL, new_mtxR, distR, imgL_gray.shape[::-1], Rot, Trns, rectify_scale,(0,0))

#### STEP 4: ###########################################################
#  Compute the mapping required to obtain the undistorted rectified stereo image pair
Left_Stereo_Map= cv2.initUndistortRectifyMap(new_mtxL, distL, rect_l, proj_mat_l,
                                             imgL_gray.shape[::-1], cv2.CV_16SC2)
Right_Stereo_Map= cv2.initUndistortRectifyMap(new_mtxR, distR, rect_r, proj_mat_r,
                                              imgR_gray.shape[::-1], cv2.CV_16SC2)

print(Left_Stereo_Map)
print(Right_Stereo_Map)
# print("Saving paraeters ......")
# cv_file = cv2.FileStorage("improved_params2.xml", cv2.FILE_STORAGE_WRITE)
# cv_file.write("Left_Stereo_Map_x",Left_Stereo_Map[0])
# cv_file.write("Left_Stereo_Map_y",Left_Stereo_Map[1])
# cv_file.write("Right_Stereo_Map_x",Right_Stereo_Map[0])
# cv_file.write("Right_Stereo_Map_y",Right_Stereo_Map[1])
# cv_file.release()


#### STEP 5: Create 3D Video ###########################################
cv2.namedWindow("Left image before rectification", cv2.WINDOW_NORMAL)
cv2.namedWindow("Right image before rectification", cv2.WINDOW_NORMAL)
cv2.namedWindow("Left image after rectification", cv2.WINDOW_NORMAL)
cv2.namedWindow("Right image after rectification", cv2.WINDOW_NORMAL)


cv2.imshow("Left image before rectification", imgL)
cv2.imshow("Right image before rectification", imgR)

Left_nice= cv2.remap(imgL,Left_Stereo_Map[0],Left_Stereo_Map[1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
Right_nice= cv2.remap(imgR,Right_Stereo_Map[0],Right_Stereo_Map[1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

cv2.imshow("Left image after rectification", Left_nice)
cv2.imshow("Right image after rectification", Right_nice)
cv2.waitKey(0)
