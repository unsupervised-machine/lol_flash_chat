from ocr.recording_modules import processing_utils
from pathlib import Path
import os

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


def test_recording_processing_runs():
    # Empty the test file out put dir
    delete_files_in_directory(directory=str(Path("tests/test_processing_utils_output")))
    # Test case for running the script while playing a league of legends match
    result = processing_utils.process_recording(program_name="League of Legends.exe",
                                                save_path_dir="tests/test_processing_utils_output",
                                                recording_delay=5,
                                                output_color="BGR",
                                                target_fps=1,
                                                save_original_image=True,
                                                save_processed_image=True,
                                                save_processed_text=True,
                                                device_number=0)
    assert result == "Successfully ran recording script"
    print("Test passed! The script runs. "
          "Check the tests/test_processing_utils_output dir to see if output files are correct.")


if __name__ == "__main__":
    test_recording_processing_runs()
