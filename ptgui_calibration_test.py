import cv2
import json
import numpy as np

import matplotlib.pyplot as plt

# INPUTS
imgL = cv2.imread("calibration_files/left_checkerboard.png")
imgR = cv2.imread("calibration_files/right_checkerboard.png")

chessboard_dims = (12,12)

with open("calibration_files/calibrationfile12x12.pts") as f:
  ptgui_dict = json.load(f)

raw_points = ptgui_dict["project"]["controlpoints"]

cornersL = []
cornersR = []
for pt in raw_points:
    l_pt = np.array([pt['0'][2:]], np.float32)
    r_pt = np.array([pt['1'][2:]], np.float32)
    cornersL.append(pt['0'][2:])
    cornersR.append(pt['1'][2:])

cornersL = np.array(cornersL, np.float32)
cornersR = np.array(cornersR, np.float32)

cv2.namedWindow("Left image before rectification", cv2.WINDOW_NORMAL)
cv2.namedWindow("Right image before rectification", cv2.WINDOW_NORMAL)
cv2.drawChessboardCorners(imgL, chessboard_dims, cornersL, True)
cv2.drawChessboardCorners(imgR, chessboard_dims, cornersR, True)
cv2.imshow("Left image before rectification", imgL)
cv2.imshow("Right image before rectification", imgR)
cv2.waitKey(0)
