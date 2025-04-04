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
    TEXT_INPUT_WIDTH = 30
    TEXT_INPUT_HEIGHT = 3
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