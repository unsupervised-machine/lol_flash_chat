# ocr/speech2text_modules/speech2text_utils.py
import numpy as np
import sounddevice as sd
import wave
import keyboard
import speech_recognition as sr
import pyautogui as pag
from time import sleep

def record_and_transcribe(talk_hotkey='m', file_name='test.wav', wave_length=2, sample_rate=16000):
    while True:
        keyboard.wait(hotkey=talk_hotkey)

        print("RECORDING ***")
        data = sd.rec(int(wave_length * sample_rate), sample_rate, channels=1)
        sd.wait()

        # Normalize
        data = data / data.max() * np.iinfo(np.int16).max

        data = data.astype(np.int16)

        with wave.open(file_name, mode='wb') as wb:
            wb.setnchannels(1)
            wb.setsampwidth(2)
            wb.setframerate(sample_rate)
            wb.writeframes(data.tobytes())

        r = sr.Recognizer()

        with sr.AudioFile(file_name) as source:
            audio_data = r.record(source)
            text = r.recognize_whisper(audio_data)
            print(text)

        keyboard.press_and_release('enter')
        sleep(0.01)
        keyboard.write(text)
        keyboard.press_and_release('enter')
