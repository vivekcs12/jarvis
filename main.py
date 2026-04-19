from voice import listen
from ai import plan
from executor import execute
from ui import start_ui
from speak import speak
import time

def run():
    while True:
        cmd = listen()

        if not cmd.startswith("jarvis"):
            continue

        cmd = cmd.replace("jarvis", "").strip()
        speak("Yes?")

        # Fast commands
        if "open chrome" in cmd:
            speak("Opening Chrome")
            execute([{"cmd":"OPEN_CHROME"}])
            continue

        if "search google" in cmd:
            query = cmd.replace("search google", "")
            speak("Searching Google")
            execute([{"cmd":"SEARCH_GOOGLE","arg":query}])
            continue

        p = plan(cmd)
        execute(p)
        time.sleep(0.5)

if __name__ == "__main__":
    start_ui(run)
