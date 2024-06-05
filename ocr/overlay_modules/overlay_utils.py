import tkinter as tk
import win32gui
import queue
import threading
import time


class CustomFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background = tk.Label(self, border=0, bg='grey15')
        self.background.pack(fill=tk.BOTH, expand=True)


class GameOverlay(tk.Tk):
    def __init__(self, text_queue):
        super().__init__()
        self.overrideredirect(True)  # Deletes Windows' default title bar
        self.wm_attributes('-alpha', 0.75)
        self.wm_attributes('-transparentcolor', 'grey15')  # Change color to avoid jagged borders
        self.wm_attributes("-topmost", True)
        self._offsetx = 0
        self._offsety = 0
        self.is_visible = True
        self.frame = None

        self.bind('<Button-1>', self.click)
        self.bind('<B1-Motion>', self.drag)
        self.bind_all('<Escape>', self.toggle_visibility)  # Bind Esc key to toggle visibility

        self.geometry("200x100+100+100")
        self.set_geometry()

        self.text_lines = []  # List to store received lines
        self.label = tk.Label(text="", font=("Helvetica", 16), fg="white", bg="black")
        self.label.pack()
        if text_queue:
            self.text_queue = text_queue
        self.update_overlay()

    def set_geometry(self):
        window_name = 'League of Legends (TM) Client'
        window_handle = win32gui.FindWindow(None, window_name)
        if window_handle:
            window_rect = win32gui.GetWindowRect(window_handle)
            print(f"League of Legends window coordinates: {window_rect}")  # Debug print for window coordinates
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            overlay_width = 300
            overlay_height = 300

            # Place the overlay 220 pixels from the right and 100 pixels from the top of the game window
            x_position = window_rect[2] - 220
            y_position = window_rect[1] + 100

            # Ensure the overlay fits within the screen boundaries
            x_position = min(x_position, screen_width - overlay_width)
            y_position = min(y_position, screen_height - overlay_height)

            self.geometry(f"{overlay_width}x{overlay_height}+{x_position}+{y_position}")
        else:
            print("League of Legends window not found.")

    def click(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def drag(self, event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry(f'+{x}+{y}')

    def toggle_visibility(self, event=None):
        if self.frame:
            self.frame.destroy()  # Destroy the frame if it exists
            self.frame = None
        else:
            self.frame = CustomFrame(self)  # Recreate the frame
            self.frame.pack(side='top', fill='both', expand=True)
            self.set_geometry()

    def update_text(self, text):
        self.text_lines.append(text)  # Append new line to the list
        self.text_lines = self.text_lines[-5:]  # Keep only the last 5 lines
        current_text = "\n".join(self.text_lines)  # Join list items to form the updated text
        self.label.config(text=current_text)

    def update_overlay(self):
        try:
            text = self.text_queue.get_nowait()
            self.update_text(text)
        except queue.Empty:
            default_text = "Default Text"
            self.update_text(default_text)

        # Schedule the update_overlay method to run again after a delay
        self.after(1000, self.update_overlay)

    def start(self):
        self.mainloop()


# helper function used for testing the overlay
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

    producer_thread = threading.Thread(target=producer, args=(text_queue,))
    producer_thread.daemon = True
    producer_thread.start()

    overlay = GameOverlay(text_queue)
    overlay.start()
