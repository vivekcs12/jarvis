import tkinter as tk
import threading, time, math

class JarvisUI:
    def __init__(self):
        self.root = tk.Tk()
        # Remove standard window decorations
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        try:
            self.root.wm_attributes("-transparentcolor", "black")
        except:
            pass

        self.root.configure(bg="black")

        # Dimensions
        self.width = 600
        self.height = 400

        # Center on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

        # Drag bindings
        self.root.bind("<B1-Motion>", self.drag_window)
        self.root.bind("<Button-1>", self.get_pos)

        # Main Canvas
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="black", highlightthickness=0)
        self.canvas.pack()

        # Center coordinates for HUD
        self.cx = 150
        self.cy = 200

        # Create futuristic HUD arcs
        self.arcs = []
        colors = ["#00ffff", "#00aaff", "#0088ff", "#0055ff"]

        # Outer ring (segmented)
        for i in range(4):
            self.arcs.append({
                'id': self.canvas.create_arc(self.cx-100, self.cy-100, self.cx+100, self.cy+100,
                                            start=i*90+10, extent=70, outline=colors[0], width=2, style=tk.ARC),
                'speed': -1.5, 'angle': i*90+10
            })

        # Middle ring
        self.arcs.append({'id': self.canvas.create_arc(self.cx-80, self.cy-80, self.cx+80, self.cy+80, start=0, extent=180, outline=colors[1], width=4, style=tk.ARC), 'speed': 2.5, 'angle': 0})
        self.arcs.append({'id': self.canvas.create_arc(self.cx-80, self.cy-80, self.cx+80, self.cy+80, start=200, extent=100, outline=colors[1], width=4, style=tk.ARC), 'speed': 2.5, 'angle': 0})

        # Inner ring (dashed effect)
        for i in range(8):
            self.arcs.append({
                'id': self.canvas.create_arc(self.cx-60, self.cy-60, self.cx+60, self.cy+60,
                                            start=i*45, extent=20, outline=colors[2], width=3, style=tk.ARC),
                'speed': -3, 'angle': i*45
            })

        # Core
        self.center_circle = self.canvas.create_oval(self.cx-20, self.cy-20, self.cx+20, self.cy+20, fill=colors[3], outline="")

        # Text Console area on the right
        self.canvas.create_rectangle(300, 50, 580, 350, outline="#00ffff", width=1)
        self.canvas.create_text(440, 40, text="SYSTEM LOG", fill="#00ffff", font=("Consolas", 10, "bold"))

        self.log_texts = []
        for i in range(12):
            text_id = self.canvas.create_text(310, 70 + (i*22), text="", fill="#00aaff", font=("Consolas", 9), anchor="w")
            self.log_texts.append(text_id)

        self.log_history = []

        # Status text below HUD
        self.status_text = self.canvas.create_text(self.cx, self.cy + 130, text="INITIALIZING...", fill="#00ffff", font=("Consolas", 12, "bold"))

        # Sub title
        self.canvas.create_text(self.cx, self.cy - 140, text="J.A.R.V.I.S. MK II", fill="#00ffff", font=("Consolas", 14, "bold"))

    def get_pos(self, event):
        self.xwin = event.x
        self.ywin = event.y

    def drag_window(self, event):
        x = self.root.winfo_pointerx() - self.xwin
        y = self.root.winfo_pointery() - self.ywin
        self.root.geometry(f"+{x}+{y}")

    def set_status(self, status):
        self.canvas.itemconfig(self.status_text, text=status)

    def add_log(self, message):
        # Truncate long messages
        if len(message) > 40:
            message = message[:37] + "..."

        self.log_history.insert(0, "> " + message)
        if len(self.log_history) > 12:
            self.log_history.pop()

        for i, text_id in enumerate(self.log_texts):
            if i < len(self.log_history):
                self.canvas.itemconfig(text_id, text=self.log_history[i])

    def animate(self):
        pulse_angle = 0
        while True:
            # Rotate arcs
            for arc in self.arcs:
                arc['angle'] = (arc['angle'] + arc['speed']) % 360
                self.canvas.itemconfig(arc['id'], start=arc['angle'])

            # Pulse center core
            pulse_size = 15 + 10 * math.sin(pulse_angle)
            self.canvas.coords(self.center_circle, self.cx - pulse_size, self.cy - pulse_size, self.cx + pulse_size, self.cy + pulse_size)
            pulse_angle += 0.15

            time.sleep(0.04)

    def start(self, run_function):
        threading.Thread(target=self.animate, daemon=True).start()
        # Pass both set_status and add_log callbacks to the main loop
        threading.Thread(target=run_function, args=(self.set_status, self.add_log), daemon=True).start()
        self.root.mainloop()

def start_ui(run_function):
    ui = JarvisUI()
    ui.start(run_function)
