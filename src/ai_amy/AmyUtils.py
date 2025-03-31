import sys
import os

def get_base_path():
    """Gets the base path for resources, whether running as script or bundled exe."""
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle (e.g., PyInstaller)
        base_path = os.path.dirname(sys.executable)
    else:
        # If the application is run as a script
        # Go up one level from the src/ai_amy directory to the project root
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


    return base_path