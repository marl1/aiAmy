from tkinter import *
import tkinter as tk

class MainWindow:
    TEXT_INPUT_WIDTH = 30
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.attributes('-topmost', True)  # Keep window on top
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.wm_attributes("-transparentcolor", "white")
        self.add_amy_picture()
        self.add_amy_text_input()
        self.update_pop_up_menu()

    def add_amy_picture(self):
        """ Create the picture of the virtual friend and the right click interaction. """
        photo = PhotoImage(file="ai_amy/img/stony.png")
        self.label = tk.Label(self.root, image=photo, bg='white')
        self.label.image = photo  # Keep a reference to prevent garbage collection
        self.label.pack(fill=tk.BOTH, expand=True)
        # https://stackoverflow.com/questions/12014210
        #On Darwin/Aqua, buttons from left to right are 1,3,2. On Darwin/X11 with recent XQuartz as the X server, they are 1,2,3; 
        self.label.bind('<Button-1>', self.register_mouse_coordinate)
        self.label.bind('<B1-Motion>', self.move_according_to_the_cursor)
        self.label.bind('<Button-2>', self.display_popup_menu)
        self.label.bind('<Button-3>', self.display_popup_menu)

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

    def add_amy_text_input(self):
            self.text_input = Text(self.root, height = 2, width = self.TEXT_INPUT_WIDTH, bg = "AntiqueWhite")
            self.text_input.pack(fill=tk.BOTH, expand=True)
            self.root.geometry(f'+{self.root.winfo_x()-self.TEXT_INPUT_WIDTH*2}+{self.root.winfo_y()}')
            self.update_pop_up_menu()

    def remove_amy_text_input(self):
        self.text_input.destroy()
        self.update_pop_up_menu()
        self.root.geometry(f'+{self.root.winfo_x()+self.TEXT_INPUT_WIDTH*2}+{self.root.winfo_y()}')