# Process and save images while in game

import dxcam
import cv2
from pathlib import Path
import time
import pytesseract
import os
import psutil
import re


# Configure project directories
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent

# Configure the path to the Tesseract executable
tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path if necessary
if not os.path.isfile(tesseract_path):
    raise FileNotFoundError(f"Tesseract executable not found at {tesseract_path}")
pytesseract.pytesseract.tesseract_cmd = tesseract_path




def is_process_running(process_name):
    # Check if there is any running process that contains the given name.
    for process in psutil.process_iter(['pid', 'name']):
        if process_name.lower() in process.info['name'].lower():
            return True
    return False


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


def image_extract_text(image):
    # try: psm 6, psm 12
    text = pytesseract.image_to_string(image, config='--psm 12')
    return text


def text_extract_lines(text):
    lines = text.split('\n')
    return lines


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


def process_latest_frame():
    target_fps = 1
    process_name = "League of Legends.exe"
    save_path = Path('data/sample_recordings/video_4')

    time.sleep(5)

    camera = dxcam.create(output_idx=0, output_color="BGR")
    camera.start(target_fps=target_fps)

    start_time_first = time.time()
    frame_count = 0

    try:
        while True:
            if not is_process_running(process_name):
                print(f"{process_name} has closed. Exiting loop.")
                break

            start_time = time.time()
            image = camera.get_latest_frame()

            # Save the original image
            cv2.imwrite(str(project_root / 'data' / 'sample_recordings' / 'video_4' / f'original_image_{frame_count}.jpg'), image)

            # Process the image
            image = image_crop_bottom_left(image)
            image = image_to_gray(image)
            image = image_binarize(image)
            text = image_extract_text(image)
            lines = text_extract_lines(text)
            lines = lines_time_stamp_filter(lines)

            # Save the processed image
            cv2.imwrite(str(project_root / 'data' / 'sample_recordings' / 'video_4' / f'processed_image_{frame_count}.jpg'), image)

            # Save the lines to a text file
            with open(project_root / 'data' / 'sample_recordings' / 'video_4' / f'lines_{frame_count}.txt', 'w') as f:
                f.write('\n'.join(lines))

            frame_count += 1

            print(f"Frame {frame_count} read:", time.time() - start_time)
            time.sleep(1 / target_fps)  # Wait for the next frame interval
    except KeyboardInterrupt:
        print("Interrupted by user. Exiting loop.")
    finally:
        camera.stop()

    print(f'Finished loop. Total time:', time.time() - start_time_first)


if __name__ == "__main__":
    process_latest_frame()

