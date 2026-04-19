import os, webbrowser, pyautogui, time
pyautogui.FAILSAFE = True

def execute(plan):
    for step in plan:
        cmd = step.get("cmd")
        arg = step.get("arg", "")

        if cmd == "OPEN_CHROME":
            os.system("start chrome")

        elif cmd == "SEARCH_GOOGLE":
            webbrowser.open(f"https://www.google.com/search?q={arg}")

        elif cmd == "TYPE":
            pyautogui.write(arg)

        elif cmd == "PRESS":
            pyautogui.press(arg)

        elif cmd == "WAIT":
            time.sleep(float(arg))

        time.sleep(1)
