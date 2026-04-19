import os, webbrowser, pyautogui, time, subprocess
from speak import speak
pyautogui.FAILSAFE = True

def execute(plan):
    for step in plan:
        cmd = step.get("cmd")
        arg = step.get("arg", "")

        try:
            if cmd == "OPEN_CHROME":
                # Handle platform differences
                if os.name == 'nt':
                    os.system("start chrome")
                else:
                    os.system("google-chrome &")

            elif cmd == "SEARCH_GOOGLE":
                webbrowser.open(f"https://www.google.com/search?q={arg}")

            elif cmd == "TYPE":
                pyautogui.write(arg)

            elif cmd == "PRESS":
                pyautogui.press(arg)

            elif cmd == "WAIT":
                time.sleep(float(arg))

            elif cmd == "RUN_CMD":
                # Execute a terminal command
                subprocess.Popen(arg, shell=True)

            elif cmd == "MOUSE_MOVE":
                # arg format: "x,y"
                coords = arg.split(",")
                if len(coords) == 2:
                    x, y = int(coords[0]), int(coords[1])
                    pyautogui.moveTo(x, y, duration=0.5)

            elif cmd == "MOUSE_CLICK":
                pyautogui.click()

            elif cmd == "OPEN_APP":
                # Open general application
                if os.name == 'nt':
                    os.system(f"start {arg}")
                else:
                    os.system(f"{arg} &")

            elif cmd == "SPEAK":
                speak(arg)

        except Exception as e:
            print(f"Error executing {cmd} with arg {arg}: {e}")

        time.sleep(0.5)
