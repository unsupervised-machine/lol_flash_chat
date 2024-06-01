# record video

import cv2
import dxcam
from pathlib import Path
import time


current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
target_fps = 10
target_duration = 5
fourcc = cv2.VideoWriter_fourcc(*'XVID')


print(dxcam.device_info())
camera = dxcam.create(output_color='BGR')

file_path = project_root / 'data' / 'sample_recordings' / f'video_3.avi'

# writer = cv2.VideoWriter(
#     str(file_path), fourcc, target_fps, (3840, 2160)
# )

out = cv2.VideoWriter(str(file_path), fourcc, target_fps, (3840, 2160))



# Start capturing frames
camera.start(target_fps=target_fps, video_mode=True)
i = 1



time.sleep(5)


while i < target_fps * target_duration:
    # Get the latest captured frame from the camera
    frame = camera.get_latest_frame()
    if frame is not None:
        # Convert the BGR frame to RGB
        # corrected_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width = frame.shape[0:2]


        # Display the corrected frame using OpenCV
        # print(f'current dir: {os.getcwd()}')

        print(f'File path: {file_path}')

        out.write(frame)

        # cv2.imshow('Corrected Frame', corrected_frame)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        i += 1

# Stop writing to video

out.release()

# Stop capturing when done
camera.stop()

# Close OpenCV windows
cv2.destroyAllWindows()
