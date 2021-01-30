# ROV-VR-Stereo-Vision
This repository contains a Python app that works with either two live camera feeds or two pre-recorded videos. It also provides a tool to compute a calibration matrix to understand the relationship between the two cameras. Once this calibration matrix is computed, it uses it to post-process the footage, merge them into a over/under stereoscopic 3D video, and outputs the 3D video output to a virtual camera for use in Unity.


## Dependencies
+ OpenCV `pip install opencv-python`
