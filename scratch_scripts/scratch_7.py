# Overlay
import pygame
import psutil
import time

import tkinter as tk
from tkinter import ttk
from time import strftime

import tkinter as tk
import win32gui


def using_pygame():
    # Constants
    OVERLAY_WIDTH = 400
    OVERLAY_HEIGHT = 100
    OVERLAY_POSITION = (100, 100)  # Position of the overlay on the screen
    FPS = 30  # Frame per second for the overlay update

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((OVERLAY_WIDTH, OVERLAY_HEIGHT), pygame.NOFRAME)
    pygame.display.set_caption('LoL Overlay')
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    # Function to find the League of Legends process
    def is_lol_running():
        return True
        # for proc in psutil.process_iter(attrs=['pid', 'name']):
        #     if 'League of Legends.exe' in proc.info['name']:
        #         return True
        # return False

    # Function to update the overlay
    def update_overlay():
        screen.fill((30, 30, 30))  # Clear the screen with a dark background
        text = font.render('League of Legends Overlay', True, (255, 255, 255))
        screen.blit(text, (10, 10))
        pygame.display.flip()


    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if is_lol_running():
            update_overlay()
        else:
            screen.fill((0, 0, 0))  # Clear the screen if the game is not running
            pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


def using_tkinter():


    # Function to update the time label
    def update_time():
        current_time = strftime('%H:%M:%S %p')
        time_label.config(text=current_time)
        time_label.after(1000, update_time)  # Update every second

    # Create the main window
    root = tk.Tk()
    root.title("League of Legends Overlay")

    # Make the window always on top
    root.attributes('-topmost', True)

    # Make the window transparent
    root.attributes('-alpha', 0.8)

    # Remove window decorations
    root.overrideredirect(True)

    # Set the window size and position
    root.geometry('200x100+10+10')

    # Add a label to display the time
    time_label = ttk.Label(root, font=('Helvetica', 20), background='black', foreground='white')
    time_label.pack(expand=True)

    # Start the time update function
    update_time()

    # Run the Tkinter event loop
    root.mainloop()


def using_similiar_to_bluepot():
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

            self.time_label_text = tk.StringVar()
            self.time_label_text.set("Game Time: 0:00")
            self.time_label = tk.Label(self, textvariable=self.time_label_text, font=('Tahoma', 12), fg='white',
                                       bg='grey15')
            self.time_label.pack(pady=20)

            self.update_time()

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

        def run(self):
            self.mainloop()

    overlay = GameOverlay()
    overlay.run()


if __name__ == "__main__":
    # using_pygame()
    # using_tkinter()
    using_similiar_to_bluepot()
