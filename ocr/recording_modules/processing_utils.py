import cv2
import pytesseract
import re
from pathlib import Path
import dxcam
import psutil
import time
from config import config
import os
from datetime import datetime, timedelta



tesseract_path = config.TESSERACT_PATH
if not os.path.isfile(tesseract_path):
    raise FileNotFoundError(f"Tesseract executable not found at {tesseract_path}")
pytesseract.pytesseract.tesseract_cmd = tesseract_path


def image_crop(image):
    """
    crops to retain only bottom left quadrant of original image
    :param image: A numpy array representing the image to be cropped.
    :return: A numpy array representing the cropped image.
    """
    # Get the dimensions of the image
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


def image_binarize(gray_image, maxValue=255, blockSize=41, C=-20):
    """
    Binarizes a grayscale image using adaptive thresholding.

    :param gray_image: A numpy array representing the grayscale image to be binarized.
    :param maxValue: The maximum value to use with the THRESH_BINARY thresholding type.
    :param blockSize: Size of the neighborhood area used to calculate the threshold value for a pixel.
    :param C: Constant subtracted from the calculated mean to fine-tune the thresholding.
    :return: A numpy array representing the binarized image.
    """

    # Apply adaptive thresholding to the grayscale image
    binary_image = cv2.adaptiveThreshold(
        gray_image,  # Input grayscale image
        maxValue=maxValue,  # Maximum value to assign to pixel values above the threshold
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # Adaptive thresholding method using a Gaussian-weighted sum
        thresholdType=cv2.THRESH_BINARY,  # Type of thresholding to apply (binary thresholding)
        blockSize=blockSize,  # Size of the neighborhood area used to calculate the threshold for each pixel
        C=C  # Constant subtracted from the mean or weighted mean
    )

    return binary_image


def image_extract_text(image):
    """
    Extracts text from an image using Optical Character Recognition (OCR).

    This function utilizes Tesseract OCR to extract text from the given image.
    It uses the Page Segmentation Mode (PSM) 12, which is designed to treat
    the image as a sparse text. If PSM 12 does not produce satisfactory results,
    consider trying PSM 6 for more standard layouts.

    :param image: A numpy array representing the image from which to extract text.
    :return: A string containing the extracted text.
    """
    # Extract text from the image using Tesseract OCR with PSM 12
    text = pytesseract.image_to_string(image, config='--psm 12')

    return text


def text_extract_lines(text):
    """
    Splits a given text into lines.

    This function takes a string of text and splits it into individual lines
    based on newline characters ('\n'). It returns a list of lines.

    :param text: A string containing the text to be split into lines.
    :return: A list of strings, where each string is a line from the original text.
    """
    lines = text.split('\n')

    return lines


def lines_time_stamp_filter(lines):
    """
    Filters lines to keep only those containing timestamps.

    This function processes a list of text lines and filters out lines
    that do not contain timestamps in the format 'xx:xx', allowing for
    optional spaces around the colon. It also ensures that any spaces
    inside the timestamps are removed and returns only the part of the
    line starting from the timestamp.

    :param lines: A list of strings, where each string is a line of text.
    :return: A list of strings containing only lines with timestamps.
    """
    # Regular expression pattern to match timestamps in the format xx:xx
    # Allows for optional spaces around the colon
    timestamp_pattern = re.compile(r'\b\d{2}\s*:\s*\d{2}\b.*$')

    # Initialize a list to store lines containing timestamps
    timestamp_lines = []

    for line in lines:
        # Remove any spaces inside of timestamps
        line = re.sub(r'\s*:\s*', ':', line, count=1)

        # Search for the timestamp pattern in the line
        match = timestamp_pattern.search(line)
        if match:
            # Extract and append the part of the line starting from the timestamp
            matched_text = line[match.start():]
            timestamp_lines.append(matched_text)

    return timestamp_lines


def lines_flash_filter(lines, minutes_to_add=5):
    """
    pipe this after the timestamp filter.
    Looks for lines that contain flash timers.
    returns the champion name and the time for when flash will be up
    :param lines:
    :return:
    """
    # Initialize a list to store lines containing timestamps
    flash_lines = []

    # Compile the regular expression pattern
    flash_pattern = re.compile(r"(\d{2}:\d{2}).*?(\w+) Flash")

    for line in lines:
        match = flash_pattern.search(line)
        if match:
            timestamp = match.group(1)
            champion_name = match.group(2)

            # Parse the timestamp and add the specified number of minutes
            original_time = datetime.strptime(timestamp, "%M:%S")
            new_time = original_time + timedelta(minutes=minutes_to_add)
            new_timestamp = new_time.strftime("%M:%S")

            # Append the modified timestamp and champion name to the result list
            flash_lines.append(f"{new_timestamp} {champion_name} Flash")

    return flash_lines


def lines_to_str(lines):
    # text = '\n'.join(lines)
    text = ' '.join(lines)
    return text



def is_process_running(process_name):
    """
        Checks if there is any running process that contains the given name.

        This function iterates over all running processes and checks if any process
        contains the specified process name (case insensitive). If a match is found,
        it returns True; otherwise, it returns False.

        :param process_name: A string representing the name of the process to search for.
        :return: A boolean value indicating whether a process with the specified name is running.
    """
    # Check if there is any running process that contains the given name.
    for process in psutil.process_iter(['pid', 'name']):
        if process_name.lower() in process.info['name'].lower():
            return True
    return False


def process_recording(program_name="League of Legends.exe",
                      save_path_dir='data/sample_recordings/untitled_recording',  # Check here for errors
                      recording_delay=5,
                      output_color="BGR",
                      target_fps=1,
                      save_original_image=True,
                      save_processed_image=True,
                      save_processed_text=True,
                      device_number=0,
                      home_dir=None,
                      text_queue=None,
                      ):
    if home_dir is not None:
        os.chdir(home_dir)

    time.sleep(recording_delay)

    camera = dxcam.create(output_idx=device_number, output_color=output_color)
    camera.start(target_fps=target_fps)

    frame_count = 0

    try:
        while True:
            if not is_process_running(process_name=program_name):
                print(f"{program_name} has closed. Exiting loop.")
                break

            image = camera.get_latest_frame()

            if save_original_image:
                cv2.imwrite(str(Path(save_path_dir) / f'original_image_{frame_count}.jpg'), image)

            # Process the Original Image to extract the relevant text
            image = image_crop(image)
            image = image_to_gray(image)
            image = image_binarize(image)
            text = image_extract_text(image)
            lines = text_extract_lines(text)
            lines = lines_time_stamp_filter(lines)
            # print(f'before flash_filter: {lines}')
            lines = lines_flash_filter(lines)

            # lines = lines_to_str(lines)

            if save_processed_image:
                cv2.imwrite(str(Path(save_path_dir) / f'processed_image_{frame_count}.jpg'), image)

            print(os.getcwd())
            if save_processed_text:
                with open(str(Path(save_path_dir) / f'lines_{frame_count}.txt'), 'w') as f:
                    f.write('\n'.join(lines))

            # print(f'text found from processing_utils: {lines}')

            if text_queue is not None:
                text_queue.put(lines)
                print(f'text put into queue {lines}')

            frame_count += 1
            print(f"Frame {frame_count} read:")
            time.sleep(1 / target_fps)  # Wait for the next frame interval
    except KeyboardInterrupt:
        print("Interrupted by user. Exiting loop.")
        return "Successfully ran recording script"
    finally:
        camera.stop()

    print(f'Finished loop.')

    return "Successfully ran recording script"
