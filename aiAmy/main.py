from loguru import logger
from tkinter import Toplevel, Tk, Label, PhotoImage

import tkinter as tk
from PIL import Image, ImageTk

def create_transparent_window():
    # Create the main window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Create a top-level window
    window = tk.Toplevel(root)
    #window.attributes('-topmost', True)  # Keep window on top
    #window.overrideredirect(True)  # Remove window decorations
    window.geometry("500x500+100+100")
    
    # Make window background transparent
    window.wm_attributes("-transparentcolor", "white")
    
    # Use PIL to open the image for better transparency support
    pil_image = Image.open("aiAmy/tux.png")
    
    # Convert image to PhotoImage
    photo = ImageTk.PhotoImage(pil_image)
    
    # Create label with transparent background
    label = tk.Label(window, image=photo, bg='white')
    label.image = photo  # Keep a reference to prevent garbage collection
    label.pack(fill=tk.BOTH, expand=True)
    
    # Optional: Make window clickthrough if needed
    #window.wm_attributes("-transparentcolor", "white")
    
    root.mainloop()

# Run the function
create_transparent_window()
