# get screen shot


import cv2
import dxcam
from pathlib import Path
import time



print(dxcam.device_info())
camera = dxcam.create()

# Start capturing frames
camera.start(target_fps=1)
i = 1


current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent

time.sleep(5)


while True:
    # Get the latest captured frame from the camera
    frame = camera.get_latest_frame()
    if frame is not None:
        # Convert the BGR frame to RGB
        corrected_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Display the corrected frame using OpenCV
        # print(f'current dir: {os.getcwd()}')
        print(f'frame height: {corrected_frame.shape[0]} \n frame width: {corrected_frame.shape[1]}')
        file_path = project_root / 'data' / 'sample_recordings' / 'recording_1' / f'image_{i}.jpg'
        print(f'File path: {file_path}')

        cv2.imwrite(str(file_path), corrected_frame)

        # cv2.imshow('Corrected Frame', corrected_frame)

        i += 1


        # Exit the loop and close the window when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Stop capturing when done
camera.stop()

# Close OpenCV windows
cv2.destroyAllWindows()
