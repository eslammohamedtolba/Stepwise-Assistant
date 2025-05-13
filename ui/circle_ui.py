import tkinter as tk
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND_COLOR, CIRCLE_COLOR,
    SPEAKING_COLOR, LISTENING_COLOR, WAVE_RADIUS, WAVE_STEP,
    WAVE_INTERVAL, WAVE_MAX, WAVE_COLORS, CLOSE_BUTTON_RADIUS,
    CLOSE_BUTTON_X, CLOSE_BUTTON_Y
)

def create_circle_ui(root, close_func):
    """Create the circular UI components"""
    # Main circular canvas
    canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, 
                    bg=BACKGROUND_COLOR, highlightthickness=0)
    
    circle_id = canvas.create_oval(5, 5, WINDOW_WIDTH-5, WINDOW_HEIGHT-5, 
                                fill=CIRCLE_COLOR, outline="")
    canvas.place(x=0, y=0)
    
    # Variables for wave animation
    wave_ovals = []
    waves_active = False
    wave_count = 0
    
    # Create close button
    close_oval_id = canvas.create_oval(
        CLOSE_BUTTON_X - CLOSE_BUTTON_RADIUS,
        CLOSE_BUTTON_Y - CLOSE_BUTTON_RADIUS,
        CLOSE_BUTTON_X + CLOSE_BUTTON_RADIUS,
        CLOSE_BUTTON_Y + CLOSE_BUTTON_RADIUS,
        fill="red", outline="", tags="close_button"
    )
    
    close_text_id = canvas.create_text(
        CLOSE_BUTTON_X, CLOSE_BUTTON_Y, 
        text="X", fill="white", 
        font=("Arial", 12, "bold"), 
        tags="close_button"
    )
    
    # Animated circle feedback with waves
    def animate_circle(mode):
        nonlocal waves_active, wave_count
        
        # Set circle color based on mode
        color = CIRCLE_COLOR
        if mode == "speaking":
            color = SPEAKING_COLOR
        elif mode == "listening":
            color = LISTENING_COLOR
        canvas.itemconfig(circle_id, fill=color)

        # Manage wave animations
        if mode in ["speaking", "listening"]:
            waves_active = True
            animate_waves(mode)
            canvas.tag_raise("close_button")
        else:
            waves_active = False
            for oval in wave_ovals:
                canvas.delete(oval)
            wave_ovals.clear()
            canvas.tag_raise("close_button")
    
    # Wave animation function
    def animate_waves(mode):
        nonlocal wave_count
        if not waves_active:
            return

        color = WAVE_COLORS.get(mode, "white")
        center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2

        if len(wave_ovals) >= WAVE_MAX:
            canvas.delete(wave_ovals[0])
            wave_ovals.pop(0)

        radius = WAVE_RADIUS + (wave_count % WAVE_MAX) * WAVE_STEP
        oval = canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            outline=color, width=2
        )
        wave_ovals.append(oval)
        wave_count += 1
        canvas.after(WAVE_INTERVAL, lambda: animate_waves(mode))
    
    # Hover effects for close button
    def on_hover(event):
        item = canvas.find_closest(event.x, event.y)
        
        if close_oval_id in item or close_text_id in item:
            canvas.itemconfig(close_oval_id, fill="darkred")
            canvas.itemconfig(close_text_id, font=("Arial", 13, "bold"))
            canvas.config(cursor="hand2")
        else:
            canvas.itemconfig(close_oval_id, fill="red")
            canvas.itemconfig(close_text_id, font=("Arial", 12, "bold"))
            canvas.config(cursor="")

    # Click event handler for the close button
    def on_click(event):
        item = canvas.find_closest(event.x, event.y)
        
        if close_oval_id in item or close_text_id in item:
            close_func()

    # Add hover and click event handlers to the canvas
    canvas.bind("<Motion>", on_hover)
    canvas.bind("<Button-1>", on_click)
    
    return animate_circle