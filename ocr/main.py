from ocr.recording_modules import processing_utils
from ocr.overlay_modules.overlay_utils import GameOverlay
from ocr.speech2text_modules import speech2text_utils
import threading
import queue


def main():
    text_queue = queue.Queue()
    custom_params = {
        "save_original_image": False,
        "save_processed_image": False,
        "save_processed_text": False,
        "recording_delay": 1,
        # Add more custom parameters as needed
    }

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
