from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk

class MainWindow:
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        #root.withdraw()  # Hide the main window

        # Create a top-level window
        #window = tk.Toplevel(root)
        self.root.attributes('-topmost', True)  # Keep window on top
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.geometry("500x500")
        
        # Make window background transparent
        self.root.wm_attributes("-transparentcolor", "white")

        
        # Use PIL to open the image for better transparency support
        pil_image = Image.open("aiAmy/img/stony.png")
        
        # Convert image to PhotoImage
        photo = ImageTk.PhotoImage(pil_image)
        
        # Create label with transparent background
        label = tk.Label(self.root, image=photo, bg='white')
        label.image = photo  # Keep a reference to prevent garbage collection
        label.pack(fill=tk.BOTH, expand=True)

        # https://stackoverflow.com/questions/12014210
        #On Darwin/Aqua, buttons from left to right are 1,3,2. On Darwin/X11 with recent XQuartz as the X server, they are 1,2,3; 
        label.bind('<Button-2>', self.display_popup)
        label.bind('<Button-3>', self.display_popup)

        self.popup = Menu(self.root, tearoff=0)
        self.popup.add_command(label="Configure") # , command=next) etc...
        self.popup.add_command(label="Previous")
        self.popup.add_separator()
        self.popup.add_command(label="Quit", command=self.root.quit)
        self.root.mainloop()
        
    #http://www.effbot.org/zone/tkinter-popup-menu.htm
    def display_popup(self, event):
        # create a popup menu
        print("popup!")
        # display the popup menu
        self.popup.tk_popup(event.x_root, event.y_root, 0)
