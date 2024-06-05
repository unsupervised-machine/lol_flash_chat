from ocr.recording_modules import processing_utils
from ocr.overlay_modules import overlay_utils
import threading
import queue


def main():
    overlay = overlay_utils.GameOverlay()
    recording_thread = threading.Thread(target=processing_utils.process_recording, kwargs={
        'queue': overlay.queue,
        'program_name': "League of Legends.exe",
        'save_path_dir': "tests/test_overlay_with_processing",
        'recording_delay': 5,
        'output_color': "BGR",
        'target_fps': 1,
        'save_original_image': True,
        'save_processed_image': True,
        'save_processed_text': True,
        'device_number': 0,
        'home_dir': r"C:\Users\Taran\Documents\projects\ocr"
    })

    recording_thread.start()
    overlay.run()
    recording_thread.join()


if __name__ == "__main__":
    main()
