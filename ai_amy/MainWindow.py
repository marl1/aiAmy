from tkinter import *
import tkinter as tk

class MainWindow:
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()

        # Create a top-level window
        self.root.attributes('-topmost', True)  # Keep window on top
        self.root.overrideredirect(True)  # Remove window decorations
        
        # Make window background transparent
        self.root.wm_attributes("-transparentcolor", "white")
        
        # Convert image to PhotoImage
        photo = PhotoImage(file="ai_amy/img/stony.png")
        
        # Create label with transparent background
        label = tk.Label(self.root, image=photo, bg='white')
        label.image = photo  # Keep a reference to prevent garbage collection
        label.pack(fill=tk.BOTH, expand=True)

        # https://stackoverflow.com/questions/12014210
        #On Darwin/Aqua, buttons from left to right are 1,3,2. On Darwin/X11 with recent XQuartz as the X server, they are 1,2,3; 
        label.bind('<B1-Motion>', self.handle_right_click)
        label.bind('<Button-2>', self.display_popup_menu)
        label.bind('<Button-3>', self.display_popup_menu)

        self.popup = Menu(self.root, tearoff=0)
        self.popup.add_command(label="Configure") # , command=next) etc...
        self.popup.add_command(label="Previous")
        self.popup.add_separator()
        self.popup.add_command(label="Quit", command=self.root.quit)
        
    #http://www.effbot.org/zone/tkinter-popup-menu.htm
    def display_popup_menu(self, event):
        # create a popup menu
        print("popup!")
        # display the popup menu
        self.popup.tk_popup(event.x_root, event.y_root, 0)
    
    def handle_right_click(self, event):
        # https://www.reddit.com/r/learnpython/nbnhx9/
        self.root.geometry(f'+{event.x_root}+{event.y_root}')
    
    def start_mainloop(self):
        self.root.mainloop()

    def set_after(self, num, func):
        self.root.after(num, func)