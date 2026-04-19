import tkinter as tk
import threading, time, math

class JarvisUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        # Transparent background for Windows/Linux
        # This can be tricky across platforms, but we'll try to support both.
        try:
            self.root.wm_attributes("-transparentcolor", "black")
        except:
            pass

        self.root.configure(bg="black")

        # Enable dragging the window
        self.root.bind("<B1-Motion>", self.drag_window)
        self.root.bind("<Button-1>", self.get_pos)

        self.root.geometry("400x400")

        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.cx, self.cy = 200, 200

        # Create multiple arcs for rotation
        self.arcs = []
        # Outer ring
        self.arcs.append({'id': self.canvas.create_arc(50, 50, 350, 350, start=0, extent=270, outline="#00ffff", width=3, style=tk.ARC), 'speed': -2, 'angle': 0})
        # Middle ring
        self.arcs.append({'id': self.canvas.create_arc(70, 70, 330, 330, start=0, extent=180, outline="#0088ff", width=5, style=tk.ARC), 'speed': 3, 'angle': 0})
        self.arcs.append({'id': self.canvas.create_arc(70, 70, 330, 330, start=200, extent=100, outline="#0088ff", width=5, style=tk.ARC), 'speed': 3, 'angle': 0})
        # Inner ring
        self.arcs.append({'id': self.canvas.create_arc(90, 90, 310, 310, start=45, extent=120, outline="#00ffff", width=2, style=tk.ARC), 'speed': -4, 'angle': 0})
        self.arcs.append({'id': self.canvas.create_arc(90, 90, 310, 310, start=225, extent=120, outline="#00ffff", width=2, style=tk.ARC), 'speed': -4, 'angle': 0})

        self.center_circle = self.canvas.create_oval(180, 180, 220, 220, fill="#00aaff", outline="")

        self.status_text = self.canvas.create_text(200, 370, text="INITIALIZING...", fill="#00ffff", font=("Consolas", 14, "bold"))
        self.sub_text = self.canvas.create_text(200, 30, text="J.A.R.V.I.S. SYSTEM ONLINE", fill="#00ffff", font=("Consolas", 10))

    def get_pos(self, event):
        self.xwin = event.x
        self.ywin = event.y

    def drag_window(self, event):
        x = self.root.winfo_pointerx() - self.xwin
        y = self.root.winfo_pointery() - self.ywin
        self.root.geometry(f"+{x}+{y}")

    def set_status(self, text):
        self.canvas.itemconfig(self.status_text, text=text)

    def animate(self):
        pulse_angle = 0
        while True:
            # Rotate arcs
            for arc in self.arcs:
                arc['angle'] = (arc['angle'] + arc['speed']) % 360
                self.canvas.itemconfig(arc['id'], start=arc['angle'])

            # Pulse center circle
            pulse_size = 15 + 8 * math.sin(pulse_angle)
            self.canvas.coords(self.center_circle, self.cx - pulse_size, self.cy - pulse_size, self.cx + pulse_size, self.cy + pulse_size)
            pulse_angle += 0.15

            time.sleep(0.04)

    def start(self, run_function):
        threading.Thread(target=self.animate, daemon=True).start()
        threading.Thread(target=run_function, args=(self.set_status,), daemon=True).start()
        self.root.mainloop()

def start_ui(run_function):
    ui = JarvisUI()
    ui.start(run_function)
