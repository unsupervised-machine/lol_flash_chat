from ocr.recording_modules import processing_utils
from pathlib import Path
import os

import threading
import queue


# Configure this test script to run from project home


# Helper function to remove files in testing directory
def delete_files_in_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                print(f"Deleted {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")


def print_queue_contents(text_queue):
    while True:
        item = text_queue.get()
        print("Queue item:", item)
        text_queue.task_done()


def test_recording_processing_runs():
    # Empty the test file out put dir
    delete_files_in_directory(directory=str(Path("tests/test_processing_utils_output")))

    # Create queue
    text_queue = queue.Queue()

    # Start thread to continuously print queue contents
    printing_thread = threading.Thread(target=print_queue_contents, args=(text_queue,))
    printing_thread.daemon = True
    printing_thread.start()

    # Test case for running the script while playing a league of legends match
    result = processing_utils.process_recording(program_name="League of Legends.exe",
                                                save_path_dir="tests/test_processing_utils_output",
                                                recording_delay=5,
                                                output_color="BGR",
                                                target_fps=1,
                                                save_original_image=True,
                                                save_processed_image=True,
                                                save_processed_text=True,
                                                device_number=0,
                                                home_dir=None,
                                                text_queue=text_queue)

    if result == "Successfully ran recording script":
        print("Test passed! The script runs. "
              "Check the tests/test_processing_utils_output dir to see if output files are correct.")


if __name__ == "__main__":
    test_recording_processing_runs()
