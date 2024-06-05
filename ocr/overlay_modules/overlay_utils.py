import tkinter as tk
import win32gui
import queue
import threading
import time


import requests
from PIL import Image, ImageTk
from io import BytesIO


# Get the latest version of the game
version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
versions = requests.get(version_url).json()
latest_version = versions[0]

# Get the champion data for the latest version
champion_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json"
champion_data = requests.get(champion_url).json()

# Extract champion names
# champion_names = {champ_data['name'] for champ_data in champion_data['data'].values()}
# Extract champion names and their icon URLs
champion_names = {}
champion_icon_urls = {}
for champ_data in champion_data['data'].values():
    champion_names[champ_data['name']] = True
    name = champ_data['name']
    icon_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/img/champion/{champ_data['image']['full']}"
    champion_icon_urls[name] = icon_url


def filter_champion_names(text_list):
    filtered_strings = [s for s in text_list if s.split()[0] in champion_names.keys()]
    # for s in text_list:
    #     name = s.split()[0]
    #     if name in champion_names.keys():
    #         print(f"{s}: Found in champion names")
    #     else:
    #         print(f"{s}: Not found in champion names")
    return filtered_strings


# function to avoid already present timers, should only keep the oldest timer less than 5 minutes old.
def remove_duplicate_timers(text_list):
    highest_times = {}
    for line in text_list:
        timer, name, summoner_spell = line.split()
        # If champ is not in dictionary or the current time is lower, update the dictionary
        if name not in highest_times or timer > highest_times[name][0]:
            highest_times[name] = (timer, summoner_spell)

    res = [f"{name} {timer} {summoner_spell}" for name, (timer, summoner_spell) in highest_times.items()]
    return res


class CustomFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background = tk.Label(self, border=0, bg='grey15')
        self.background.pack(fill=tk.BOTH, expand=True)


class GameOverlay(tk.Tk):
    def __init__(self, text_queue):
        super().__init__()
        self.label_widgets = []
        self.overrideredirect(True)  # Deletes Windows' default title bar
        self.wm_attributes('-alpha', 0.75)
        self.wm_attributes('-transparentcolor', 'grey15')  # Change color to avoid jagged borders
        self.wm_attributes("-topmost", True)
        self._offsetx = 0
        self._offsety = 0
        self.is_visible = True
        # self.frame = None
        self.canvas = None
        self.scrollable_frame = None

        self.bind('<Button-1>', self.click)
        self.bind('<B1-Motion>', self.drag)
        self.bind_all('<Escape>', self.toggle_visibility)  # Bind Esc key to toggle visibility

        self.geometry("200x100+100+100")
        self.set_geometry()

        self.text_lines = []  # List to store received lines
        self.label = tk.Label(text="Flash Timer Overlay", font=("Helvetica", 16), fg="white", bg="black")
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
            overlay_width = 600
            overlay_height = 1000

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

    # def toggle_visibility(self, event=None):
    #     if self.frame:
    #         self.frame.destroy()  # Destroy the frame if it exists
    #         self.frame = None
    #     else:
    #         self.frame = CustomFrame(self)  # Recreate the frame
    #         self.frame.pack(side='top', fill='both', expand=True)
    #         self.set_geometry()
    def toggle_visibility(self, event=None):
        if self.canvas:
            self.canvas.destroy()  # Destroy the canvas if it exists
            self.canvas = None
        else:
            self.create_canvas()  # Recreate the canvas
            self.set_geometry()

    def create_canvas(self):
        self.canvas = tk.Canvas(self, bg='grey15', highlightthickness=0)
        self.canvas.pack(side='left', fill='both', expand=True)

        self.scrollable_frame = tk.Frame(self.canvas, bg='grey15')
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')

        def configure_scroll_region(event):
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        self.scrollable_frame.bind('<Configure>', configure_scroll_region)

        scrollbar = tk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        scrollbar.pack(side='right', fill='y')
        self.canvas.config(yscrollcommand=scrollbar.set)

    def get_champion_icons(self):
        pass

    def update_text(self, text_list):
        max_lines = 5
        unique_lines = []

        for line in text_list:
            if line not in self.text_lines:
                unique_lines.append(line)  # Filter out duplicates

        self.text_lines.extend(unique_lines)  # Extend the list with new unique lines

        # Remove excess lines if necessary
        if len(self.text_lines) > max_lines:
            self.text_lines = self.text_lines[-max_lines:]

        # Clear existing labels
        for widget_tuple in self.label_widgets:
            champ_icon_label, text_label = widget_tuple
            champ_icon_label.destroy()
            text_label.destroy()

        self.label_widgets = []

        # Create new labels for each line of text
        for i, line in enumerate(self.text_lines):
            champ_name, timer, summoner_spell = line.split()

            icon_url = champion_icon_urls[champ_name]
            image_bytes = requests.get(icon_url).content
            champ_image = Image.open(BytesIO(image_bytes))
            champ_image = champ_image.resize((40, 40))
            champ_photo = ImageTk.PhotoImage(champ_image)
            champ_icon_label = tk.Label(self.scrollable_frame, image=champ_photo)
            champ_icon_label.image = champ_photo
            champ_icon_label.pack(side='top', anchor='w', padx=5, pady=5)

            text_label = tk.Label(self.scrollable_frame, text=f"{timer} {summoner_spell}", font=("Helvetica", 16))
            text_label.pack(side='top', anchor='w', padx=5, pady=5)

            self.label_widgets.append((champ_icon_label, text_label))

    def update_overlay(self):
        try:
            text_list = self.text_queue.get_nowait()
            print(f"text_list: {text_list}")
            text_list = remove_duplicate_timers(text_list)
            text_list = filter_champion_names(text_list)
            self.update_text(text_list)
        except queue.Empty:
            pass
            # default_text = "Default Text"
            # self.update_text(default_text)

        # Schedule the update_overlay method to run again after a delay
        self.after(1000, self.update_overlay)

    def start(self):
        self.mainloop()


# function used for testing the overlay
def producer(queue_obj):
    counter = 0
    while True:
        counter += 1
        lines = [f"Line {counter}-{i}" for i in range(5)]  # Create a list of strings
        # print(f"Text from queue: {lines}")
        queue_obj.put(lines)  # Put the list of strings into the queue
        time.sleep(1)  # Adjust the sleep duration as needed





if __name__ == "__main__":
    text_queue = queue.Queue()

    producer_thread = threading.Thread(target=producer, args=(text_queue,))
    producer_thread.daemon = True
    producer_thread.start()

    overlay = GameOverlay(text_queue)
    overlay.start()
