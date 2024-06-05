import queue
import tkinter as tk
import win32gui


class CustomFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background = tk.Label(self, border=0, bg='grey15')
        self.background.pack(fill=tk.BOTH, expand=True)


class GameOverlay(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

        self.lines = ["Champ 1: 0", "Champ 2: 0", "Champ 3: 0", "Champ 4: 0", "Champ 5: 0"]

        self.time_label_text = tk.StringVar()
        self.time_label_text.set("Game Time: 0:00")
        self.time_label = tk.Label(self, textvariable=self.time_label_text, font=('Tahoma', 12), fg='white',
                                   bg='grey15')
        self.time_label.pack(pady=20)

        self.queue = queue.Queue()

        # self.update_time()
        self.update_text()

    def set_geometry(self):
        window_name = 'League of Legends (TM) Client'
        window_handle = win32gui.FindWindow(None, window_name)
        if window_handle:
            window_rect = win32gui.GetWindowRect(window_handle)
            print(f"League of Legends window coordinates: {window_rect}")  # Debug print for window coordinates
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            overlay_width = 300
            overlay_height = 450

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
            self.time_label.pack(pady=20)

    def update_time(self):
        # This function should update the game time periodically
        # Here we just increment the time for demonstration purposes
        current_time = self.time_label_text.get().split(" ")[-1]
        minutes, seconds = map(int, current_time.split(":"))
        seconds += 1
        if seconds == 60:
            minutes += 1
            seconds = 0
        # self.time_label_text.set(f"Game Time: {minutes}:{seconds:02d}")
        self.time_label_text.set(f"{minutes}:{seconds:02d}")
        self.after(1000, self.update_time)

    def update_text(self):
        print(self.lines)
        try:
            while True:
                lines = self.queue.get_nowait()  # Get lines from the queue if available
                self.lines = lines  # Update self.lines with new lines
                self.time_label_text.set("\n".join(self.lines))
        except queue.Empty:
            pass
        self.after(1000, self.update_text)  # Schedule the next update after 1 second

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    overlay = GameOverlay()
    overlay.run()

