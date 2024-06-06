from ocr.recording_modules import processing_utils
from ocr.overlay_modules.overlay_utils import GameOverlay
from ocr.speech2text_modules import speech2text_utils
import threading
import queue
import psutil
import time


TARGET_PROCESS_NAME = "League of Legends.exe"


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


def main():
    text_queue = queue.Queue()
    custom_params = {
        "save_original_image": False,
        "save_processed_image": False,
        "save_processed_text": False,
        "recording_delay": 1,
        # Add more custom parameters as needed
    }
    while True:

        if not is_process_running(TARGET_PROCESS_NAME):
            print("Target process is not running. Terminating all scripts.")
            return

        # Start the recording processing thread
        producer_thread = threading.Thread(target=processing_utils.process_recording, kwargs={"text_queue": text_queue, **custom_params})
        producer_thread.daemon = True
        producer_thread.start()

        # Start the speech-to-text thread
        speech_to_text_thread = threading.Thread(target=speech2text_utils.record_and_transcribe)
        speech_to_text_thread.daemon = True
        speech_to_text_thread.start()

        # Start the game overlay in the main thread
        overlay = GameOverlay(text_queue)
        overlay.start()



        # Wait for the threads to finish
        producer_thread.join()
        speech_to_text_thread.join()


if __name__ == "__main__":
    main()
