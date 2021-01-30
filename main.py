import cv2
import numpy as np
import pyvirtualcam
import time

l_vid = cv2.VideoCapture("test_footage/left-footage.MOV")
r_vid = cv2.VideoCapture("test_footage/right-footage.MOV")

l_framespersecond= int(l_vid.get(cv2.CAP_PROP_FPS))
r_framespersecond= int(r_vid.get(cv2.CAP_PROP_FPS))

print("Left FPS: ", l_framespersecond)
print("Right FPS: ", r_framespersecond)

i = 0

with pyvirtualcam.Camera(width=3840, height=4320, fps=100) as virtual_cam:
    while(True):
        t1 = time.time()

        # Capture frame-by-frame
        l_ret, l_frame = l_vid.read()
        r_ret, r_frame = r_vid.read()

        t2 = time.time()
        print("T1: ", t2-t1)

        # # Our operations on the frame come here
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        stacked_frame = np.vstack([l_frame, r_frame])
        t3 = time.time()
        print("T2: ", t3-t2)

        # print("Resolution: ", stacked_frame.shape)
        # print(i)
        i += 1

        t4 = time.time()
        print("T3: ", t4-t3)

        # Send resulting frame to virtual camera
        frame = np.zeros((virtual_cam.height, virtual_cam.width, 4), np.uint8) # RGBA
        t5 = time.time()
        print("T4: ", t5-t4)

        frame[:,:,:3] = stacked_frame#virtual_cam.frames_sent % 255 # grayscale animation
        # frame[:,:,3] = 255
        t6 = time.time()
        print("T5: ", t6-t5)

        virtual_cam.send(frame) # Note: this seems to lag based on set fps
        t7 = time.time()
        print("T6: ", t7-t6)
        # virtual_cam.sleep_until_next_frame()













        # cv2.imshow("Left image before rectification", imgL)
        # cv2.imshow("Right image before rectification", imgR)
        #
        # Left_nice= cv2.remap(imgL,Left_Stereo_Map[0],Left_Stereo_Map[1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
        # Right_nice= cv2.remap(imgR,Right_Stereo_Map[0],Right_Stereo_Map[1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
        #
        # cv2.imshow("Left image after rectification", Left_nice)
        # cv2.imshow("Right image after rectification", Right_nice)
        # cv2.waitKey(0)



        # # Display the resulting frame
        # cv2.namedWindow("over-under frame", cv2.WINDOW_NORMAL)
        # cv2.imshow("over-under frame", stacked_frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
