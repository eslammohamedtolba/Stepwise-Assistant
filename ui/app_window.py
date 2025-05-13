import os
import tkinter as tk
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, 
    WINDOW_POSITION_X, WINDOW_POSITION_Y,
    BACKGROUND_COLOR
)
from ui.circle_ui import create_circle_ui

def create_app_window():
    """Create and configure the main application window"""
    root = tk.Tk()
    
    # Configure window properties
    root.overrideredirect(True)
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{WINDOW_POSITION_X}+{WINDOW_POSITION_Y}")
    root.configure(bg=BACKGROUND_COLOR)
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-transparentcolor", BACKGROUND_COLOR)
    
    # Draggable window logic
    def start_move(event):
        root.x = event.x
        root.y = event.y

    def do_move(event):
        x = event.x_root - root.x
        y = event.y_root - root.y
        root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

    root.bind("<Button-1>", start_move)
    root.bind("<B1-Motion>", do_move)
    
    # Close function
    def close():
        root.destroy()
        os._exit(0)
    
    # Create circular UI
    animate_circle = create_circle_ui(root, close)
    
    return root, animate_circle