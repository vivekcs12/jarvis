import tkinter as tk
import threading, time, math

def start_ui(run_function):
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.wm_attributes("-transparentcolor", "black")
    root.configure(bg="black")
    root.geometry("300x300")

    canvas = tk.Canvas(root, width=300, height=300, bg="black", highlightthickness=0)
    canvas.pack()

    outer = canvas.create_oval(50,50,250,250, outline="#00ffff")
    line = canvas.create_line(150,150,150,70, fill="cyan")

    def animate():
        angle = 0
        while True:
            x = 150 + 80 * math.cos(angle)
            y = 150 + 80 * math.sin(angle)
            canvas.coords(line,150,150,x,y)
            angle += 0.05
            time.sleep(0.04)

    threading.Thread(target=animate, daemon=True).start()
    threading.Thread(target=run_function, daemon=True).start()

    root.mainloop()
