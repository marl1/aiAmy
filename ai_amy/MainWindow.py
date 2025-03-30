from tkinter import *
import tkinter as tk
from tkinter import scrolledtext
from ScrollableReadOnlyText import *
from AmyController import *
from itertools import count
from ImageLabel import *
import AmyAnimation

class MainWindow:
    TEXT_INPUT_WIDTH = 30
    TEXT_INPUT_HEIGHT = 3
    TEXT_OUTPUT_WIDTH = 30
    TEXT_OUTPUT_HEIGHT = 5
    def __init__(self, amy_controller):
        self.amy_controller = amy_controller
        # Create the main window
        self.root = tk.Tk()
        self.root.attributes('-topmost', True)  # Keep window on top
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.wm_attributes("-transparentcolor", "white")
        self.add_amy_picture()
        self.add_amy_text_output()
        self.add_amy_text_input()
        self.root.bind("<Configure>", self.update_following_windows_position)
        self.update_pop_up_menu()
        self.root.geometry('200x100')

    def add_amy_picture(self):
        """ Create the picture of the virtual friend and the right click interaction. """
        self.label = ImageLabel(self.root,  bg='white')
        self.label.load("ai_amy/img/stonyMove.gif")
        self.label.pack(fill=tk.BOTH, expand=True)
        # https://stackoverflow.com/questions/12014210
        #On Darwin/Aqua, buttons from left to right are 1,3,2. On Darwin/X11 with recent XQuartz as the X server, they are 1,2,3; 
        self.label.bind('<Button-1>', self.register_mouse_coordinate)
        self.label.bind('<B1-Motion>', self.move_according_to_the_cursor)
        self.label.bind('<Button-2>', self.display_popup_menu)
        self.label.bind('<Button-3>', self.display_popup_menu)
        self.amy_animation = AmyAnimation.AmyAnimation(self.label)

    def update_pop_up_menu(self):
        """ Adds or removes elements from the popup menu (by creating a new menu) """
        self.popup = Menu(self.root, tearoff=0)
        self.popup.add_command(label="Configure") # , command=next) etc...
        if(self.text_input.winfo_exists()):
            self.popup.add_command(label="Hide text input", command=self.remove_amy_text_input)
        else:
            self.popup.add_command(label="Show text input", command=self.add_amy_text_input)
        self.popup.add_separator()
        self.popup.add_command(label="Quit", command=self.root.quit)

    #http://www.effbot.org/zone/tkinter-popup-menu.htm
    def display_popup_menu(self, event):
        # display the popup menu
        self.popup.tk_popup(event.x_root, event.y_root, 0)
    
    def register_mouse_coordinate(self, event):
        self.mouse_rclick_x = event.x
        self.mouse_rclick_y = event.y

    def move_according_to_the_cursor(self, event):
        # https://www.reddit.com/r/learnpython/nbnhx9/
        x_position=event.x_root - self.mouse_rclick_x
        y_position=event.y_root - self.mouse_rclick_y
        self.root.geometry(f'+{x_position}+{y_position}')
    
    def start_mainloop(self):
        self.root.mainloop()

    def set_after(self, num, func):
        self.root.after(num, func)

    def add_amy_text_output(self):
        """ Adds a separate window that follows the main window. It contains the
        text the character will say."""
        # Create a separate top-level window for the text input
        self.text_output_window = tk.Toplevel(self.root)
        self.text_output_window.attributes('-alpha', 0.7)
        self.text_output_window.overrideredirect(True)  # Remove window decorations
        self.text_output_window.attributes('-topmost', True)

        self.text_output = ScrollableReadOnlyText(self.text_output_window, width=30, height=4)
        self.text_output.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        self.text_output.set_content("Hello from Amy !")

    def update_following_windows_position(self, event=None):
        """ To make the text input and out windows follow the character. """
        if hasattr(self, 'text_input_window') and self.text_input_window.winfo_exists():
            x = self.root.winfo_x() - self.TEXT_INPUT_WIDTH * 2
            y = self.root.winfo_y()
            self.text_input_window.geometry(f'+{x+45}+{y+self.root.winfo_height()}')
        if hasattr(self, 'text_output_window') and self.text_output_window.winfo_exists():
            x = self.root.winfo_x() - self.TEXT_INPUT_WIDTH * 2
            y = self.root.winfo_y()
            self.text_output_window.geometry(f'+{x+58}+{y-self.text_output_window.winfo_height()+40}')

###### all about inputting text #######
    def add_amy_text_input(self):
        """ Adds a separate window that follows the main window. It contains a text area for
        the user to write in."""
        # Create a separate top-level window for the text input
        self.text_input_window = tk.Toplevel(self.root)
        self.text_input_window.overrideredirect(True)  # Remove window decorations
        self.text_input_window.attributes('-topmost', True)
        self.text_input_window.attributes('-alpha', 0.1)
        
        # Position the text window relative to the main window
        x = self.root.winfo_x() - self.TEXT_INPUT_WIDTH * 2
        y = self.root.winfo_y()
        
        self.text_input = Text(self.text_input_window, height=1, 
                            width=self.TEXT_INPUT_WIDTH, bg="White")
        self.text_input.pack(fill=tk.BOTH, expand=True)
        
        self.update_pop_up_menu()
        self.text_input.bind('<Return>', self.send_text)
        self.text_input.bind('<KeyRelease-Return>', self.clear_input_text)
        self.text_input.bind('<Shift-Return>', lambda event: print(""))
        self.text_input.bind("<FocusIn>", self.make_opaque_amy_text_input)
        self.text_input.bind("<FocusOut>", self.make_transparent_amy_text_input)
        

    def make_opaque_amy_text_input(self, event):
        self.text_input_window.attributes('-alpha', 1)
        self.text_input.configure(height=self.TEXT_INPUT_HEIGHT)

    def make_transparent_amy_text_input(self, event):
        self.text_input_window.attributes('-alpha', 0.1)
        self.text_input.configure(height=1)

    def remove_amy_text_input(self):
        self.text_input_window.destroy()
        self.update_pop_up_menu()

    def send_text(self, event):
        self.amy_controller.send_text(self.text_input.get('1.0', 'end').rstrip())
        self.text_input.delete('1.0', END) # Clear the text but \n will be added just after
    
    def clear_input_text(self, event):
        if(self.text_input.get('1.0', 'end').strip()==""):
            self.text_input.delete('1.0', END)