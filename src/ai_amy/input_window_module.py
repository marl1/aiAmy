from tkinter import *
import tkinter as tk
from tkinter import scrolledtext
from ScrollableReadOnlyText import *
import AmyController
from itertools import count
from ImageLabel import *
import AmyAnimation

class InputWindow:

    TEXT_INPUT_WIDTH = 30
    TEXT_INPUT_HEIGHT = 3
    
    def __init__(self, main_window_root: Tk, amy_controller: AmyController):
        """ Adds a separate window that follows the main window. It contains a text area for
            the user to write in."""
        self.amy_controller=amy_controller
        # Create a separate top-level window for the text input
        self.frame = tk.Toplevel(main_window_root)
        self.frame.overrideredirect(True)  # Remove window decorations
        self.frame.attributes('-topmost', True)
        self.frame.attributes('-alpha', 0.1)
        self.text_input = Text(self.frame, height=1, 
                            width=self.TEXT_INPUT_WIDTH, bg="White")
        self.text_input.pack(fill=tk.BOTH, expand=True)
        
        
        self.text_input.bind('<Return>', self.send_text)
        self.text_input.bind('<KeyRelease-Return>', self.clear_input_text)
        self.text_input.bind('<Shift-Return>', lambda event: print(""))
        self.text_input.bind("<FocusIn>", self.make_opaque_amy_text_input)
        self.text_input.bind("<FocusOut>", self.make_transparent_amy_text_input)
        

    def make_opaque_amy_text_input(self, event):
        self.frame.attributes('-alpha', 1)
        self.text_input.configure(height=self.TEXT_INPUT_HEIGHT)

    def make_transparent_amy_text_input(self, event):
        self.frame.attributes('-alpha', 0.1)
        self.text_input.configure(height=1)

    def remove_amy_text_input(self):
        self.frame.destroy()

    def send_text(self, event):
        self.amy_controller.send_text(self.text_input.get('1.0', 'end').rstrip())
        self.text_input.delete('1.0', END) # Clear the text but \n will be added just after
        self.frame.focus()
    
    def clear_input_text(self, event):
        if(self.text_input.get('1.0', 'end').strip()==""):
            self.text_input.delete('1.0', END)

    def follow_main_window_position(self, main_window_x, main_window_y, main_window_height):
        x = main_window_x - self.TEXT_INPUT_WIDTH * 2
        y = main_window_y
        self.frame.geometry(f'+{x+45}+{y+main_window_height}')