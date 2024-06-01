# Extracting text from videos and images

from pathlib import Path
import cv2
import pytesseract
from PIL import Image
import numpy as np
import re
import os
import time



# Configure project directories
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent

# Configure the path to the Tesseract executable
tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path if necessary
if not os.path.isfile(tesseract_path):
    raise FileNotFoundError(f"Tesseract executable not found at {tesseract_path}")
pytesseract.pytesseract.tesseract_cmd = tesseract_path

# Configure Video Path
video_input_path = project_root / 'data' / 'sample_recordings' / f'video_2.avi'
video_frames_output_folder = project_root / 'data' / 'sample_recordings' / f'video_2'

# Configure Image Path
image_input_path = video_frames_output_folder / 'frame_0000.jpg'

# Configure Text Path
text_output_path = ''


def video_extract_frames(video_path, output_folder, frame_rate=1):
    # Create the output folder if it doesn't exist
    output_folder.mkdir(parents=True, exist_ok=True)

    # Capture the video from the file
    print(f'video_path: {video_path}')
    print(f'str(video_path): {str(video_path)}')
    video_capture = cv2.VideoCapture(str(video_path))

    # Get the frames per second (fps) of the video
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    print(f'video frame rate: {fps}')

    # Calculate the interval between frames to capture
    interval = int(fps / frame_rate)

    frame_count = 0
    saved_count = 0

    while True:
        # Read a frame
        ret, frame = video_capture.read()

        if not ret:
            break

        # Save the frame if it is at the specified interval
        if frame_count % interval == 0:
            frame_filename = output_folder / f"frame_{saved_count:04d}.jpg"
            cv2.imwrite(str(frame_filename), frame)
            saved_count += 1

        frame_count += 1

    # Release the video capture object
    video_capture.release()


def image_display(image, window_name='Image'):
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def image_crop_bottom_left(image):
    height, width = image.shape[0], image.shape[1]
    # Calculate the coordinates for the bottom-left quadrant
    start_row = height // 2
    end_row = height
    start_col = 0
    end_col = width // 2
    # Crop the image using array slicing
    cropped_image = image[start_row:end_row, start_col:end_col]
    return cropped_image


def image_to_gray(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray


def adaptive_threshold_trackbars(gray_image,
                                 block_size_range=(3, 51),
                                 C_range=(-50,50),
                                 adaptive_method=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 max_value=255
                                 ):
    raise NotImplementedError("This function is not implemented yet.")


def image_binarize(gray_image,
                   maxValue=255,
                   blockSize=41,
                   C=-20
                   ):
    binary_image = cv2.adaptiveThreshold(
        gray_image,
        maxValue=maxValue,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY,
        blockSize=blockSize,  # Size of the neighborhood area
        C=C  # Constant subtracted from the weighted mean
    )
    return binary_image


def image_blur(image, kernel_size=(1, 1), sigma=0):
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    return blurred


def image_edges(gray_image):
    edges = cv2.Canny(gray_image, 50, 150)
    return edges


def image_contours(canny_image):
    contours = cv2.findContours(canny_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    return contours


def image_filter_contours(canny_image):
    raise NotImplementedError("This function is not implemented yet.")


def image_morph_open(image):
    raise NotImplementedError("This function is not implemented yet.")


def image_extract_text(image):
    # try: psm 6, psm 12
    text = pytesseract.image_to_string(image, config='--psm 12')
    return text


def text_display(text):
    print(text)


def text_extract_lines(text):
    lines = text.split('\n')
    return lines


def lines_display(lines):
    for i, line in enumerate(lines):
        print(f'line {i}: {line}')


def lines_time_stamp_filter(lines):
    # try:
    # re.compile(r'\b[^\s]{2}:[^\s]{2}\b')
    # re.compile(r'\b\d{2}:\d{2}\b.*$')
    # Regular expression pattern to match timestamps in the format xx:xx ( ignores single space between colon )
    # re.compile(r'\b\d{2}\s*:\s*\d{2}\b.*$')

    timestamp_pattern = re.compile(r'\b\d{2}\s*:\s*\d{2}\b.*$')

    # Filter lines to keep only those containing timestamps
    # timestamp_lines = [line for line in lines if timestamp_pattern.search(line)]
    timestamp_lines = []
    for line in lines:
        # remove non-word and non-space characters
        # line = re.sub(r'[^\w\s]+$', '', line)
        # remove any spaces inside of timestamps
        line = re.sub(r'\s*:\s*', ':', line, count=1)

        match = timestamp_pattern.search(line)
        if match:
            matched_text = line[match.start():]
            timestamp_lines.append(matched_text)

    return timestamp_lines


def text_remove_bad_character(text):
    raise NotImplementedError("This function is not implemented yet.")


def text_check_spelling(text):
    raise NotImplementedError("This function is not implemented yet.")


def test_basic_functionality():
    # Testing Functions
    # Extracting Frames from Videos
    video_extract_frames(video_input_path, video_frames_output_folder)

    # Loading and Transforming Images
    test_image = cv2.imread(str(image_input_path))
    test_image = image_crop_bottom_left(test_image)
    test_image = image_to_gray(test_image)
    test_image = image_binarize(test_image)
    # image_display(test_image)

    # Extracting Text from Images
    test_text = image_extract_text(test_image)
    text_display(test_text)
    return None


def test_processing_text():
    start_time = time.time()
    test_image = cv2.imread(str(image_input_path))
    test_image = image_crop_bottom_left(test_image)
    test_image = image_to_gray(test_image)
    test_image = image_binarize(test_image)
    # image_display(test_image, 'binary_image')

    test_text = image_extract_text(test_image)
    # text_display(test_text)

    test_lines = text_extract_lines(test_text)
    # lines_display(test_lines)

    test_lines = lines_time_stamp_filter(test_lines)
    lines_display(test_lines)


def test_processing_speed():
    start_time_first = time.time()
    test_image = cv2.imread(str(image_input_path))
    print("image_read:", time.time() - start_time_first)

    start_time = time.time()
    test_image = image_crop_bottom_left(test_image)
    print("image_crop_bottom_left:", time.time() - start_time)

    start_time = time.time()
    test_image = image_to_gray(test_image)
    print("image_to_gray:", time.time() - start_time)

    start_time = time.time()
    test_image = image_binarize(test_image)
    print("image_binarize:", time.time() - start_time)

    # image_display(test_image, 'binary_image')

    start_time = time.time()
    test_text = image_extract_text(test_image)
    print("image_extract_text:", time.time() - start_time)

    # text_display(test_text)

    start_time = time.time()
    test_lines = text_extract_lines(test_text)
    print("text_extract_lines:", time.time() - start_time)

    # lines_display(test_lines)

    start_time = time.time()
    test_lines = lines_time_stamp_filter(test_lines)
    print("lines_time_stamp_filter:", time.time() - start_time)

    print("Total Time:", time.time() - start_time_first)
    lines_display(test_lines)




if __name__ == '__main__':
    # test_basic_functionality()
    # test_processing_text()
    test_processing_speed()

