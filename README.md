# ROV-VR-Stereo-Vision
This repository contains a Python app that works with either two live camera feeds or two pre-recorded videos. It also provides a tool to compute a calibration matrix to understand the relationship between the two cameras. Once this calibration matrix is computed, it uses it to post-process the footage, merge them into a over/under stereoscopic 3D video, and outputs the 3D video output to a virtual camera for use in Unity.


## Dependencies
+ OpenCV: `pip install opencv-python`
+ [pyvirtualcam](https://pypi.org/project/pyvirtualcam/): `pip install pyvirtualcam`
        + Download the "OBS-VirtualCamX.X.X.zip" option from [this site](https://github.com/CatxFish/obs-virtual-cam/releases)
        + Open an administrative command prompt
        + Navigate to the directory
        + Run these lines in the window
        ```
regsvr32 /n /i:1 "obs-virtualcam\bin\32bit\obs-virtualsource.dll"
regsvr32 /n /i:1 "obs-virtualcam\bin\64bit\obs-virtualsource.dll"
        ```

Notes:
+ there's two virtual cameras - OBS Virtual Camera and OBS-Camera. OBS Virtual Camera comes from the new OBS update and works with zoom but not Unity, and OBS-Camera comes from the registry edit and works with Unity but not zoom. Go figure

## Setup
+ Download one pair of left/right footage samples from this link https://drive.google.com/drive/folders/1QPG4X94ZUW1u5V7Ym5SMQ_sy2J49Zhlm?usp=sharing
+ Make sure the name matches the file path the script references
+ Run the main script
+ Run the ROV-VR app in unity and select OBS-Camera


# Shenanigans
C:\Program Files\obs-studio\obs-plugins\32bit


+ Note: OBS must be installed and the registry must be edited - follow the instructions listed [here](https://pypi.org/project/pyvirtualcam/)
    + Install OBS Studio ([reference](https://obsproject.com/welcome))
        + Select "I will only be using the virtual camera" during the install process
    + Install OBS Virtual Cam ([reference](https://github.com/Fenrirthviti/obs-virtual-cam/releases))
