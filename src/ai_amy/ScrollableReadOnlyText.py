import tkinter as tk

#Big thanks to Claude.ai for that class
class ScrollableReadOnlyText:
    def __init__(self, master, width=20, height=1):
        self.frame = tk.Frame(master)
        
        # Create a Text widget
        self.text = tk.Text(
            self.frame,
            width=width,
            height=height,
            wrap=tk.WORD,
            font=('Arial', 10),
            relief="flat",
            borderwidth=0,
            highlightthickness = 0,
            cursor="arrow",
            padx=3,
            pady=3
        )             
        
        # Create a Scrollbar that will always exist but be visible only when needed
        self.scrollbar = tk.Scrollbar(self.frame, command=self.text.yview)
        self.text.configure(yscrollcommand=self.update_scrollbar)
        
        # Grid layout for stability
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.text.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Initially hide scrollbar (without removing it from layout)
        self.scrollbar.grid_remove()        
        self.text.bind("<<Modified>>", self.on_content_modified)
        self.set_read_only()
    
    def update_scrollbar(self, first, last):
        # Update scrollbar position
        self.scrollbar.set(first, last)
        
        # Check if scrollbar is needed based on position values
        if float(first) > 0.0 or float(last) < 1.0:
            # Content is scrollable
            if not self.scrollbar.winfo_ismapped():
                self.scrollbar.grid()
        else:
            # Content fits without scrolling
            if self.scrollbar.winfo_ismapped():
                self.scrollbar.grid_remove()
    
    def on_content_modified(self, event=None):
        if(len(self.text.get('1.0', 'end'))>80):
            self.text.configure(height=5)
        elif(len(self.text.get('1.0', 'end'))>40):
            self.text.configure(height=2)
        else:
            self.text.configure(height=1)
        self.text.edit_modified(False)
        self.check_scrollbar_needed()
    
    def check_scrollbar_needed(self):
        # Get the first and last visible positions
        first, last = self.text.yview()
        
        # Update scrollbar visibility based on these positions
        if first > 0.0 or last < 1.0:
            self.scrollbar.grid()
        else:
            self.scrollbar.grid_remove()
    
    def set_content(self, content):
        # Enable editing temporarily
        self.text.config(state=tk.NORMAL)
        
        # Clear existing content and insert new content
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.INSERT, content)
        
        # Make it read-only again
        self.set_read_only()
        
        # Check scrollbar visibility
        self.check_scrollbar_needed()
    
    def set_read_only(self):
        self.text.config(state=tk.DISABLED)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)
    
    def place(self, **kwargs):
        self.frame.place(**kwargs)