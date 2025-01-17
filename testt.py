import cv2
import numpy as np


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Fail to open the camera...")
else:
    while True:
        ret, frame = cap.read() # ret >> bool; frame >> piece of video
        if not ret:
            print("Error")
            break
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)       
        cv2.imshow("frame", frame)

        if (cv2.waitKey(1) & 0xFF == ord('p') or cv2.waitKey(1) & 0xFF == ord('P')):
            screen_shot = frame
            gary_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)      
            cv2.imshow("Screen Capture", gary_frame)

            cv2.waitKey(1)
                
        if (cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == ord('Q')): #0xFF stand for all platforms is work
            break
cap.release()
cv2.destroyAllWindows()
import cv2
import numpy as np

def generate_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Failed to open the camera.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        _, jpeg_gray = cv2.imencode('.jpg', gray_frame)
        gray_bytes = jpeg_gray.tobytes()
        
        yield gray_bytes  # 灰階畫面
    
    cap.release()

frames_generator = generate_frames()

try:
    first_frame = next(frames_generator)
    print(f"First frame size: {len(first_frame)} bytes")
except StopIteration:
    print("No more frames.")

