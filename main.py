import cv2
import numpy as np
import pyvirtualcam
import time
from msvcrt import kbhit # Reading keyboard input
from msvcrt import getch # Reading keyboard input

l_vid_path = "test_footage/left-footage.mp4"
r_vid_path = "test_footage/right-footage.mp4"

l_vid = cv2.VideoCapture(l_vid_path)
r_vid = cv2.VideoCapture(r_vid_path)

# print(l_vid)

l_vid.set(1,3000)
r_vid.set(1,3000)


l_framespersecond= int(l_vid.get(cv2.CAP_PROP_FPS))
r_framespersecond= int(r_vid.get(cv2.CAP_PROP_FPS))

print("Left FPS: ", l_framespersecond)
print("Right FPS: ", r_framespersecond)

i = 0

calibration_filename = "results.txt"
# Load previous calibration (Image offsets, in pixels)
f = open(calibration_filename, 'r')
data = f.readlines()
dx = int(data[1])
dy = int(data[3])

# Adjustment increment (in pixels)
increment = 10

with pyvirtualcam.Camera(width=3840, height=4320, fps=100) as virtual_cam:
    while(True):
        t1 = time.time()

        # Capture frame-by-frame
        l_ret, l_frame = l_vid.read()
        r_ret, r_frame = r_vid.read()

        # Restart video if we're out of frames
        if not l_ret and not r_ret:
            print("Restarting video")
            l_vid = cv2.VideoCapture(l_vid_path)
            r_vid = cv2.VideoCapture(r_vid_path)

            l_ret, l_frame = l_vid.read()
            r_ret, r_frame = r_vid.read()

            t2 = time.time()
            print("T1: ", t2-t1)

        # Process user input ---------------------------------------------------
        if kbhit():
            user_input = getch()

            # Press q to quit
            if user_input == b'q':
                break

            # Press s to save
            elif user_input == b's':
                f = open("results.txt", "w")
                f.write("X Translation:\n")
                f.write(str(dx) + "\n")
                f.write("Y Translation:\n")
                f.write(str(dy) + "\n")
                f.close()
                print("Saved offsets!")

            # Arrow keys start with b'\xe0'
            elif user_input == b'\xe0':
                arrowkey = getch()
                if arrowkey == b'H':
                    print("Shifting up")
                    dy -= increment
                elif arrowkey == b'P':
                    print("Shifting down")
                    dy += increment
                elif arrowkey == b'K':
                    print("Shifting left")
                    dx -= increment
                elif arrowkey == b'M':
                    print("Shifting right")
                    dx += increment

        # Shift right frame ---------------------------------------------------
        print(r_frame.shape)
        rows, cols, _ = r_frame.shape
        M = np.float32([[1,0,dx],
                        [0,1,dy]])

        r_shifted = cv2.warpAffine(r_frame, M, (cols,rows))

        # Stack images  -------------------------------------------------------
        stacked_frame = np.vstack([l_frame, r_shifted])

        # Send resulting frame to virtual camera
        frame = np.zeros((virtual_cam.height, virtual_cam.width, 4), np.uint8) # RGBA
        frame[:,:,:3] = stacked_frame
        virtual_cam.send(frame) # Note: this seems to lag based on set fps

cv2.destroyAllWindows()
