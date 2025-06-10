import tkinter as tk
from tkinter import ttk
from tkinter import font
import queue

# --- Constants for easy color management ---
PRIMARY_COLOR = "#007ACC"
BUTTON_BG_NORMAL = "white"
BUTTON_BG_ACTIVE = "#005999"
TEXT_COLOR_NORMAL = PRIMARY_COLOR
TEXT_COLOR_ACTIVE = "white"
CLOSE_BUTTON_COLOR = "#FF3B30"
CHAT_BG = "#2B2B2B"
AI_SENDER_COLOR = "#57A6FF"
USER_SENDER_COLOR = "#34D399"

# --- Scrollbar dark theme colors ---
SCROLLBAR_TROUGH = "#2E2E2E"
SCROLLBAR_KNOB = "#555555"
SCROLLBAR_KNOB_ACTIVE = "#676767"
ARROW_COLOR = "#999999"

class ChatWindow(tk.Toplevel):
    def __init__(self, master, pos_x, pos_y, on_send_callback, on_close_callback, on_minimize_callback):
        super().__init__(master)
        self.on_send_callback = on_send_callback
        self.on_close_callback = on_close_callback
        self.on_minimize_callback = on_minimize_callback

        self.overrideredirect(True)
        self.geometry(f"400x550+{pos_x}+{pos_y}")
        self.configure(bg=CHAT_BG)
        self.wm_attributes("-topmost", True)

        self.bind("<FocusOut>", self.handle_focus_out)

        style = ttk.Style(self)
        style.theme_use('clam')
        
        style.configure("Dark.Vertical.TScrollbar", gripcount=0, troughcolor=SCROLLBAR_TROUGH, bordercolor=SCROLLBAR_TROUGH, background=SCROLLBAR_KNOB, arrowcolor=ARROW_COLOR)
        style.map("Dark.Vertical.TScrollbar", background=[('active', SCROLLBAR_KNOB_ACTIVE)])
        
        style.configure("Custom.TEntry", padding=(10, 8, 10, 8), relief="flat", background="#3C3C3C", fieldbackground="#3C3C3C", foreground="white", insertcolor="white")
        style.map("Custom.TEntry", fieldbackground=[('focus', '#3C3C3C')], relief=[('focus', 'flat')])

        header = tk.Frame(self, bg="#1E1E1E", height=40)
        header.pack(fill="x")
        header.bind("<ButtonPress-1>", self.start_move)
        header.bind("<ButtonRelease-1>", self.stop_move)
        header.bind("<B1-Motion>", self.do_move)

        title_label = tk.Label(header, text="AI Chat Assistant", bg="#1E1E1E", fg="white", font=("Arial", 11, "bold"))
        title_label.pack(side="left", padx=10)
        title_label.bind("<ButtonPress-1>", self.start_move)
        title_label.bind("<ButtonRelease-1>", self.stop_move)
        title_label.bind("<B1-Motion>", self.do_move)

        close_button = tk.Button(header, text="✕", bg="#1E1E1E", fg="white", font=("Arial", 12, "bold"), relief="flat", command=self.close_window)
        close_button.pack(side="right", padx=10)
        
        minimize_button = tk.Button(header, text="—", bg="#1E1E1E", fg="white", font=("Arial", 12, "bold"), relief="flat", command=self.minimize_window)
        minimize_button.pack(side="right", padx=10)
        
        conversation_frame = tk.Frame(self, bg=CHAT_BG)
        conversation_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.scrollbar = ttk.Scrollbar(conversation_frame, orient="vertical", style="Dark.Vertical.TScrollbar")
        self.text_area = tk.Text(conversation_frame, bg=CHAT_BG, fg="white", font=("Arial", 12), wrap="word", relief="flat", state="disabled", yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)
        
        self.scrollbar.pack(side="right", fill="y")
        self.text_area.pack(side="left", fill="both", expand=True)

        input_frame = tk.Frame(self, bg=CHAT_BG, pady=5)
        input_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.entry = ttk.Entry(input_frame, style="Custom.TEntry", font=("Arial", 12))
        self.entry.pack(fill="x", expand=True, side="left")
        self.entry.bind("<Return>", self.send_message)

        send_button = tk.Button(input_frame, text="➤", bg=PRIMARY_COLOR, fg="white", font=("Arial", 14, "bold"), relief="flat", command=self.send_message, height=1)
        send_button.pack(side="right", padx=(5, 0), fill="y")

    def handle_focus_out(self, event):
        # Only minimize if focus is truly lost from the entire app, not just moving between widgets.
        if self.focus_get() is None:
            self.minimize_window()

    def insert_with_bold(self, text_area, line):
        import re
        pattern = r"\*\*(.*?)\*\*"  # matches **bold**
        idx = 0
        for match in re.finditer(pattern, line):
            start, end = match.span()
            # Insert text before bold part
            if start > idx:
                text_area.insert(tk.END, line[idx:start])
            # Insert bold part
            bold_text = match.group(1)
            text_area.insert(tk.END, bold_text, "bold")
            idx = end
        # Insert remaining text
        if idx < len(line):
            text_area.insert(tk.END, line[idx:])

    def format_message(self, text_area, message):
        import re

        # Define tag styles (ensure this is only done once in your init)
        text_area.tag_configure("bold", font=font.Font(weight="bold"))
        text_area.tag_configure("bullet", lmargin1=15, lmargin2=30)

        # Split by lines to handle bullets
        for line in message.splitlines():
            # Match bullet points
            if re.match(r"^\* ", line):
                content = line[2:].strip()
                text_area.insert(tk.END, "• ", "bullet")
                self.insert_with_bold(text_area, content)
                text_area.insert(tk.END, "\n")
            else:
                self.insert_with_bold(text_area, line)
                text_area.insert(tk.END, "\n")

    def add_message(self, sender, message):
        self.text_area.config(state="normal")

        sender_font = font.Font(family="Arial", size=12, weight="bold")

        if sender == "AI":
            tag_name = "ai_sender"
            color = AI_SENDER_COLOR
        else:
            tag_name = "user_sender"
            color = USER_SENDER_COLOR

        self.text_area.tag_configure(tag_name, font=sender_font, foreground=color)

        self.text_area.insert(tk.END, f"{sender}: ", tag_name)

        # 👇 Format and insert message with styling
        self.format_message(self.text_area, message)

        self.text_area.insert(tk.END, "\n")
        self.text_area.config(state="disabled")
        self.text_area.see(tk.END)

    def start_move(self, event): self.x = event.x; self.y = event.y
    def stop_move(self, event): self.x = None; self.y = None
    def do_move(self, event): self.geometry(f"+{self.winfo_x() + event.x - self.x}+{self.winfo_y() + event.y - self.y}")
    def minimize_window(self):
        if self.on_minimize_callback: self.on_minimize_callback()
        self.withdraw()
    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if user_input:
            self.entry.delete(0, tk.END)
            if self.on_send_callback: self.on_send_callback(user_input)
    def close_window(self):
        if self.on_close_callback: self.on_close_callback()
        self.destroy()

class FloatingCircle(tk.Tk):
    def __init__(self, input_queue, output_queue):
        super().__init__()
        self.chat_window = None
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.minimized_chat_icon = None # Start with no icon widget

        self.overrideredirect(True)
        
        window_width = 160
        window_height = 160
        screen_width = self.winfo_screenwidth()
        x = screen_width - window_width - 50 
        y = 50 
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-transparentcolor", "black")

        self.canvas = tk.Canvas(self, width=160, height=160, bg="black", highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_oval(5, 5, 155, 155, fill=PRIMARY_COLOR, outline="")

        self.create_circular_close_button(68, 12, 12, self.quit_app)
        self.write_button_info = self.create_oval_button(25, 105, 50, 28, "Chat", self.open_chat)
        self.speak_button_info = self.create_oval_button(85, 105, 50, 28, "Speak", self.speak_placeholder)
        
        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<ButtonRelease-1>", self.stop_move)
        self.canvas.bind("<B1-Motion>", self.do_move)
        
        self.process_incoming_messages()

    def process_incoming_messages(self):
        while not self.output_queue.empty():
            try:
                sender, message = self.output_queue.get(0)
                if sender == "__EXIT__":
                    self.quit_app()
                    return
                if self.chat_window and self.chat_window.winfo_exists():
                    self.chat_window.add_message(sender, message)
            except queue.Empty:
                pass
        self.after(100, self.process_incoming_messages)

    def handle_user_input(self, user_input):
        self.input_queue.put(user_input)

    def create_oval_button(self, x, y, width, height, text, command):
        button_canvas = tk.Canvas(self, width=width, height=height, bg=PRIMARY_COLOR, highlightthickness=0)
        button_canvas.create_oval(0, 0, width-1, height-1, fill=BUTTON_BG_NORMAL, outline="")
        button_canvas.create_text(width/2, height/2, text=text, fill=TEXT_COLOR_NORMAL, font=("Arial", 10, "bold"))
        button_canvas.bind("<Button-1>", lambda event: command())
        button_canvas.bind("<Enter>", lambda e: button_canvas.config(cursor="hand2"))
        button_canvas.bind("<Leave>", lambda e: button_canvas.config(cursor=""))
        button_canvas.place(x=x, y=y)
        return button_canvas, None, None # Return value not used, simplified

    def create_circular_close_button(self, x, y, radius, command):
        btn_canvas = tk.Canvas(self, width=radius*2, height=radius*2, bg=PRIMARY_COLOR, highlightthickness=0)
        btn_canvas.create_oval(0, 0, radius*2, radius*2, fill=CLOSE_BUTTON_COLOR, outline="")
        btn_canvas.create_text(radius, radius, text="✕", fill="white", font=("Arial", int(radius*0.8), "bold"))
        btn_canvas.bind("<Button-1>", lambda e: command())
        btn_canvas.bind("<Enter>", lambda e: btn_canvas.config(cursor="hand2"))
        btn_canvas.bind("<Leave>", lambda e: btn_canvas.config(cursor=""))
        btn_canvas.place(x=x, y=y)

    def start_move(self, event): self.x = event.x; self.y = event.y
    def stop_move(self, event): self.x = None; self.y = None
    def do_move(self, event): self.geometry(f"+{self.winfo_x() + event.x - self.x}+{self.winfo_y() + event.y - self.y}")

    def on_chat_close(self):
        canvas, _, _ = self.write_button_info
        canvas.itemconfig(1, fill=BUTTON_BG_NORMAL) # 1 is the ID of the oval
        canvas.itemconfig(2, fill=TEXT_COLOR_NORMAL) # 2 is the ID of the text
        
        # --- FIX: If the icon exists, destroy it and nullify the variable ---
        if self.minimized_chat_icon:
            self.minimized_chat_icon.destroy()
            self.minimized_chat_icon = None
        
        self.chat_window = None
        self.input_queue.put("__RESET__")

    def handle_chat_minimize(self):
        if self.chat_window and self.chat_window.winfo_viewable():
            # --- FIX: Only create the icon if it doesn't already exist ---
            if not self.minimized_chat_icon:
                self.minimized_chat_icon = tk.Label(self, text="💬", bg=PRIMARY_COLOR, fg=BUTTON_BG_NORMAL, font=("Segoe UI Emoji", 18), cursor="hand2")
                self.minimized_chat_icon.bind("<Button-1>", lambda e: self.restore_chat())
            self.minimized_chat_icon.place(x=35, y=65)

    def restore_chat(self):
        if self.chat_window:
            # --- FIX: Destroy the icon when restoring the chat ---
            if self.minimized_chat_icon:
                self.minimized_chat_icon.destroy()
                self.minimized_chat_icon = None

            circle_x, circle_y = self.winfo_x(), self.winfo_y()
            chat_width, margin = 400, 20
            
            if circle_x - margin - chat_width > 0:
                pos_x = circle_x - chat_width - margin
            else:
                pos_x = circle_x + self.winfo_width() + margin

            pos_y = circle_y
            self.chat_window.geometry(f"+{pos_x}+{pos_y}")
            self.chat_window.deiconify()
            self.chat_window.entry.focus_set()

    def open_chat(self):
        if self.chat_window and self.chat_window.winfo_exists():
            if not self.chat_window.winfo_viewable(): self.restore_chat()
            else: self.chat_window.lift()
            return
        
        circle_x, circle_y = self.winfo_x(), self.winfo_y()
        chat_width, margin = 400, 20

        if circle_x - margin - chat_width > 0:
            pos_x = circle_x - chat_width - margin
        else:
            pos_x = circle_x + self.winfo_width() + margin
        
        pos_y = circle_y
        
        self.chat_window = ChatWindow(self, pos_x, pos_y, 
            on_send_callback=self.handle_user_input, 
            on_close_callback=self.on_chat_close,
            on_minimize_callback=self.handle_chat_minimize)
        
        self.output_queue.put(("AI", "Hello! How can I assist you today?"))
        
        self.chat_window.entry.focus_set()

        canvas, _, _ = self.write_button_info
        canvas.itemconfig(1, fill=BUTTON_BG_ACTIVE)
        canvas.itemconfig(2, fill=TEXT_COLOR_ACTIVE)

    def speak_placeholder(self):
        if self.chat_window and self.chat_window.winfo_exists():
            self.output_queue.put(("System", "Voice input is not yet implemented."))

    def quit_app(self):
        self.input_queue.put("__EXIT__")
        self.after(200, self.destroy)
