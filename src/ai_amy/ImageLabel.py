import tkinter as tk
from PIL import Image, ImageTk, ImageSequence # Added ImageSequence
from itertools import count
import io # Needed if passing bytes

# From https://stackoverflow.com/questions/43770847
# Improved by Gemini 2.5 experimental pro 03-25
class ImageLabel(tk.Label):
    """
    A Tkinter Label widget that displays images and plays animated GIFs.
    Handles variable frame durations and proper cancellation of animation loops.
    """
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._frames = []
        self._delays = []
        self._loc = 0
        self._after_id = None

    def load(self, im, backup_delay=100):
        """
        Load an image or animated GIF.

        Args:
            im: Path to the image file (str), a file-like object,
                or a PIL.Image object.
            backup_delay (int): Default delay in milliseconds per frame
                                if not specified in GIF metadata.
        """
        # --- Stop any previous animation ---
        self._stop_animation()
        self._reset_state()

        try:
            # --- Load image using PIL ---
            img = None # Initialize img to None
            if isinstance(im, str):
                # Load from file path
                img = Image.open(im)
            elif hasattr(im, 'read'):
                 # Load from file-like object (e.g., BytesIO)
                img = Image.open(im)
            elif isinstance(im, Image.Image):
                # Use provided PIL Image object directly
                img = im
            else:
                raise TypeError("Unsupported image source type")

            # --- Extract frames and delays ---
            if getattr(img, "is_animated", False):
                # Handle animated GIFs
                for frame in ImageSequence.Iterator(img):
                    self._frames.append(ImageTk.PhotoImage(frame.copy()))
                    # Get duration, default if missing or 0
                    duration = frame.info.get('duration', backup_delay)
                    if duration <= 10: # Some viewers interpret 0/1 as 100ms
                         duration = backup_delay
                    self._delays.append(duration)
                # Reset internal PIL pointer if we used ImageSequence
                if hasattr(img, 'seek'):
                    img.seek(0)

            else:
                # Handle static images
                self._frames.append(ImageTk.PhotoImage(img.copy()))
                self._delays.append(backup_delay) # Not used, but keep lists parallel

            # --- Display first frame ---
            if self._frames:
                self.config(image=self._frames[0])

            # --- Start animation if multiple frames ---
            if len(self._frames) > 1:
                self._start_animation()

        except Exception as e:
            print(f"Error loading image: {e}")
            # Optionally display a placeholder/error image or clear the label
            self.unload()
        finally:
            # Close the image file if we opened it from a path or stream
            # Check if img is not None and has a close method
            if isinstance(im, (str)) and img and hasattr(img, 'close'):
                 img.close()
            elif hasattr(im, 'read') and img and hasattr(img, 'close'):
                 # Avoid closing if it was passed as an already open Image object
                 # The responsibility to close is on the caller in that case
                 pass


    def _reset_state(self):
        """Clear internal state."""
        self.config(image=None) # Clear current image display
        self._frames = []
        self._delays = []
        self._loc = 0
        # self._after_id is handled by _stop_animation

    def _stop_animation(self):
        """Cancel any pending animation frame."""
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None

    def _start_animation(self):
        """Start the animation loop."""
        self._next_frame()

    def _next_frame(self):
        """Display the next frame in the animation sequence."""
        if not self._frames: # Check if unloaded during delay
            return

        # Move to the next frame index
        self._loc = (self._loc + 1) % len(self._frames)

        # Update the image displayed
        self.config(image=self._frames[self._loc])

        # Schedule the next frame update
        delay = self._delays[self._loc]
        self._after_id = self.after(delay, self._next_frame)

    def unload(self):
        """Stop animation and clear the displayed image."""
        self._stop_animation()
        self._reset_state()

    def __del__(self):
        """Attempt to stop animation when the object is destroyed."""
        try:
            self._stop_animation()
        except: # Ignore errors during destruction
             pass