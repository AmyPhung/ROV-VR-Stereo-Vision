import cv2
import numpy as np

l_vid = cv2.VideoCapture("test_footage/left-footage.MOV")
r_vid = cv2.VideoCapture("test_footage/right-footage.MOV")

while(True):
    # Capture frame-by-frame
    l_ret, l_frame = l_vid.read()
    r_ret, r_frame = r_vid.read()

    # # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    stacked = np.vstack([l_frame, r_frame])
    print("Resolution: ", stacked.shape)

    # Display the resulting frame
    cv2.namedWindow("over-under frame", cv2.WINDOW_NORMAL)
    cv2.imshow("over-under frame", stacked)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
