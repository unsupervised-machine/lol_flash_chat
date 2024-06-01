
import cv2
import pytesseract
from PIL import Image
import numpy as np
import re
import os

# Configure the path to the Tesseract executable
tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path if necessary
if not os.path.isfile(tesseract_path):
    raise FileNotFoundError(f"Tesseract executable not found at {tesseract_path}. Please install Tesseract or update the path.")
pytesseract.pytesseract.tesseract_cmd = tesseract_path


# Function to display images
def display_image(image, window_name='Image'):
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def crop_image_bottom_left(image):
    height, width = image.shape[0], image.shape[1]
    # Calculate the coordinates for the bottom-left quadrant
    start_row = height // 2
    end_row = height
    start_col = 0
    end_col = width // 2
    # Crop the image using array slicing
    cropped_image = image[start_row:end_row, start_col:end_col]
    return cropped_image


# Load and preprocess the image
image_path = '../data/sample_images/1a632458-3836-4eec-8baa-f37ff8cbd44c.jpg'
image_path = '../data/sample_images/1e031aff-6d59-444a-9895-05443581cf89.jpg'
image_path = '../data/sample_images/1d3f2959-8178-4e79-bd58-e3ade14ebd7c.jpg'
image_path = '../data/sample_images/flashping_1.JPG'




image = cv2.imread(image_path)
if image is None:
    raise FileNotFoundError(f"Image file not found at {image_path}.")
display_image(image, "Original Image")

# Crop Image
image = crop_image_bottom_left(image)
display_image(image, "Cropped Image")


# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
display_image(gray, window_name="Grayscale Image")

# Blur image
# blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
# display_image(blurred_image, window_name='Blurred Image')

# Edge Detection
# edges = cv2.Canny(gray, 50, 150)
# display_image(edges, window_name="Grayscale Image")


# Apply thresholding to get a binary image
# binary_image = cv2.adaptiveThreshold(
#     gray,
#     maxValue=255,
#     adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#     thresholdType=cv2.THRESH_BINARY,
#     blockSize=31,  # Size of the neighborhood area
#     C=5  # Constant subtracted from the weighted mean
# )
# display_image(binary_image, window_name="Binary Image")


def adaptive_threshold_trackbars(image,
                                 block_size_range=(3, 51),
                                 C_range=(-50,50),
                                 adaptive_method=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 max_value=255
                                 ):
    cv2.namedWindow('Adaptive Thresholding')

    # Function to update the thresholded image based on trackbar changes
    def update_threshold(x):
        block_size = cv2.getTrackbarPos('Block Size', 'Adaptive Thresholding')
        if block_size % 2 == 0:
            block_size += 1  # Ensure block_size is odd
        if block_size < block_size_range[0]:
            block_size = block_size_range[0]  # Ensure minimum block_size

        C = cv2.getTrackbarPos('C', 'Adaptive Thresholding') - 50

        thresh_image = cv2.adaptiveThreshold(image, max_value, adaptive_method,
                                             cv2.THRESH_BINARY, block_size, C)
        cv2.imshow('Adaptive Thresholding', thresh_image)

    # Calculate the initial positions for block size and C
    initial_block_size = max(3, (block_size_range[1] + block_size_range[0]) // 2)
    if initial_block_size % 2 == 0:
        initial_block_size += 1
    initial_C = (C_range[1] - C_range[0]) // 2 + 50

    # Create trackbars for block size and C
    cv2.createTrackbar('Block Size', 'Adaptive Thresholding', initial_block_size, block_size_range[1], update_threshold)
    cv2.createTrackbar('C', 'Adaptive Thresholding', initial_C, 100, update_threshold)

    # Initial call to the update function
    update_threshold(0)

    # Wait until the user presses a key
    cv2.waitKey(0)
    cv2.destroyAllWindows()


adaptive_threshold_trackbars(gray, block_size_range=(3, 51), C_range=(0, 50))


# Apply thresholding to get a binary image
# Looks like the best parameter values were  block size: 32, C: 32
binary_image = cv2.adaptiveThreshold(
    gray,
    maxValue=255,
    adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    thresholdType=cv2.THRESH_BINARY,
    blockSize=41,  # Size of the neighborhood area
    C=-20  # Constant subtracted from the weighted mean
)
display_image(binary_image, window_name="Binary Image")
display_image(image, window_name="Original Image")

# Remove noise and smooth the image
# Not sure if any of this is really helping
# Opening is just another name of erosion followed by dilation. It is useful in removing noise.
kernel = np.ones((1, 1), np.uint8)
opening = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel, iterations=1)
display_image(opening, window_name="Opened Image")


# median_filtered_image = cv2.medianBlur(eroded_image, 1)
# display_image(eroded_image, window_name="Median Filtered Image")

# Perform OCR
text = pytesseract.image_to_string(binary_image, config='--psm 6')
print(text)

# Clean Text
cleaned_text = re.sub(r'[^A-Za-z0-9\s]', '', text)
print(cleaned_text)

# Note it looks like tesseract might not be great for hand writen data try another model






