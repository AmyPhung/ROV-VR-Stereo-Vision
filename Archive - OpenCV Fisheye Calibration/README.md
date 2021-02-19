# ROV-VR-Stereo-Vision
This repository contains a Python app that takes in either two live camera feeds or two pre-recorded videos, and outputs the stereo video output to a virtual camera for use in Unity.

## Video Footage

https://drive.google.com/drive/u/0/folders/1QPG4X94ZUW1u5V7Ym5SMQ_sy2J49Zhlm
test_footage/left-footage.MOV
test_footage/right-footage.MOV

https://drive.google.com/file/d/1oyrj3s0IVu_A55uJlvWYdRd2qgDmTUax/view?usp=sharing
test_footage/D1306_Smith_110120.mp4

## Dependencies
+ Python (tested using 3.8.3)
+ OpenCV: `pip install opencv-python`
+ [pyvirtualcam](https://pypi.org/project/pyvirtualcam/): `pip install pyvirtualcam`
  + Note: OBS must be installed and the registry must be edited - based on [these instructions](https://pypi.org/project/pyvirtualcam/)
      + Install OBS Studio ([reference](https://obsproject.com/welcome))
          + Select "I will only be using the virtual camera" during the install process
      + Make a registry edit by running the file reg_path.reg from [here](https://github.com/CatxFish/obs-virtual-cam/releases/tag/1.2.1))

## Usage
+ `prestitched-footage.py` -"Gold standard" footage
+ `unstitched-footage.py` - Arrow keys

## Notes:
+ there's two virtual cameras - OBS Virtual Camera and OBS-Camera. OBS Virtual Camera comes from the new OBS update and works with zoom but not Unity, and OBS-Camera comes from the registry edit and works with Unity but not zoom which is a bit odd.
