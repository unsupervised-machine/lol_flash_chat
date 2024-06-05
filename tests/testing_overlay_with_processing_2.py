from ocr.recording_modules import processing_utils
from pathlib import Path
import os
from ocr.overlay_modules.overlay_utils import GameOverlay

import threading
import queue
import time


# Configure this test script to run from project home


# Function to remove files in testing directory
# def delete_files_in_directory(directory):
#     for filename in os.listdir(directory):
#         file_path = os.path.join(directory, filename)
#         try:
#             if os.path.isfile(file_path):
#                 os.unlink(file_path)
#                 print(f"Deleted {file_path}")
#         except Exception as e:
#             print(f"Error deleting {file_path}: {e}")
#
#
# def print_queue_contents(text_queue):
#     while True:
#         item = text_queue.get()
#         print("Queue item:", item)
#         text_queue.task_done()

# Function to populate the queue for testing
def producer(queue_obj):
    counter = 0
    while True:
        counter += 1
        text = f"Line {counter}"
        print(f"text from queue: {text}")
        queue_obj.put(text)
        time.sleep(1)  # Adjust the sleep duration as needed


if __name__ == "__main__":
    text_queue = queue.Queue()
    custom_params = {
        "save_original_image": False,
        "save_processed_image": False,
        "save_processed_text": False,
        # Add more custom parameters as needed
    }

    producer_thread = threading.Thread(target=processing_utils.process_recording, kwargs={"text_queue": text_queue, **custom_params})
    producer_thread.daemon = True
    producer_thread.start()

    overlay = GameOverlay(text_queue)
    overlay.start()
