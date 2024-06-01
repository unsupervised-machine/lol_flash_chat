# Processing images from live video stream

import dxcam
import cv2
from pathlib import Path
import time
import pytesseract
import os


# Configure project directories
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent

# Configure the path to the Tesseract executable
tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path if necessary
if not os.path.isfile(tesseract_path):
    raise FileNotFoundError(f"Tesseract executable not found at {tesseract_path}")
pytesseract.pytesseract.tesseract_cmd = tesseract_path







class VideoRecorder:
    def __init__(self):
        self.camera = dxcam.create(output_idx=0, output_color="BGR")
        self.target_fps = 10
        self.target_duration = 5
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.output_file = project_root / 'data' / 'sample_recordings' / f'video_4.avi'
        self.video_writer = self.set_video_writer()
        self.frame_size = self.set_frame_size()

    def set_video_writer(self):
        return cv2.VideoWriter(str(self.output_file), self.fourcc, self.target_fps, self.frame_size)

    def set_frame_size(self):
        # Numpy images are given by height, width
        # cv2 images are given by width, weight
        # we need the images in the cv2 format for VideoWriter
        image = self.camera.grab()
        height, width = image.shape[0:2]
        frame_size = (width, height)
        return frame_size

    def start_recording(self):
        # self.camera.start(target_fps=self.target_fps, video_mode=True)
        raise NotImplementedError("This function is not implemented yet.")


def test_camera_is_capturing():
    camera = dxcam.create(output_color='BGR')
    print(f'camera is capturing: {camera.is_capturing}')
    camera.start()
    print(f'camera is capturing: {camera.is_capturing}')
    camera.stop()
    print(f'camera is capturing: {camera.is_capturing}')


def test_get_frame_size():
    camera = dxcam.create(output_idx=0, output_color="BGR")
    image = camera.grab()
    print(f'dimensions: {image.shape[0:2]}')
    # cv2.imshow('image', image)
    # cv2.waitKey(0)


def test_camera_get_latest_frame():
    # This tests that get_latest_frame is working by taking 1 ima
    title = "[DXcam] Capture benchmark"
    target_fps = 5
    duration_seconds = 10
    n_frames = target_fps * duration_seconds

    time.sleep(5)

    camera = dxcam.create(output_idx=0, output_color="BGR")
    # camera.start(target_fps=target_fps, video_mode=True)
    camera.start(target_fps=target_fps)

    # writer = cv2.VideoWriter(
    #     "video.avi", cv2.VideoWriter_fourcc(*'XVID'), target_fps, (3840, 2160)
    # )
    for i in range(n_frames):
        # writer.write(camera.get_latest_frame())
        image = camera.get_latest_frame()
        cv2.imwrite(str(project_root / 'data' / 'sample_recordings' / 'video_4' / f'image_{i}.jpg'), image)
    camera.stop()
    # writer.release()


def process_latest_frame():
    target_fps = 5
    duration_seconds = 10
    n_frames = target_fps * duration_seconds

    time.sleep(5)

    camera = dxcam.create(output_idx=0, output_color="BGR")
    camera.start(target_fps=target_fps)

    start_time_first = time.time()
    for i in range(n_frames):
        start_time = time.time()
        image = camera.get_latest_frame()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(image, config='--psm 12')
        # print(text)
        cv2.imwrite(str(project_root / 'data' / 'sample_recordings' / 'video_4' / f'image_{i}.jpg'), image)

        print(f"frame {i} read:", time.time() - start_time)

    print(f'finished loop', time.time() - start_time_first)
    camera.stop()


if __name__ == "__main__":
    # test_camera_is_capturing()
    # test_get_frame_size()
    # test_camera_get_latest_frame()
    process_latest_frame()
