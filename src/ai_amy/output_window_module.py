from tkinter import *
import tkinter as tk
from tkinter import scrolledtext
from ScrollableReadOnlyText import *
from AmyController import *
from itertools import count
from ImageLabel import *
import AmyAnimation

class OutputWindow:
    """ A separate window that follows the main window. It contains the
        text the character will say."""
    TEXT_OUTPUT_WIDTH = 30
    TEXT_OUTPUT_HEIGHT = 5
    def __init__(self, main_window_root: Tk):
        self.frame = tk.Toplevel(main_window_root)
        self.frame.attributes('-alpha', 0.7)
        self.frame.overrideredirect(True)  # Remove window decorations
        self.frame.attributes('-topmost', True)

        self.text = ScrollableReadOnlyText(self.frame, width=30, height=4)
        self.text.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        self.text.set_content("Hello from Amy !")

    def follow_main_window_position(self, main_window_x, main_window_y, main_window_height):
            x = main_window_x - self.TEXT_OUTPUT_WIDTH * 2
            y = main_window_y
            self.frame.geometry(f'+{x+58}+{y-self.frame.winfo_height()+config.get().get_config_output_window_y_offset()}')

    def set_text(self, text):
         self.text.set_content(text)
