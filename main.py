from voice import listen
from ai import plan
from executor import execute
from ui import start_ui
from speak import speak
import time

def run(set_status):
    set_status("READY")
    while True:
        set_status("WAITING FOR TRIGGER...")
        cmd = listen()

        if not cmd:
            continue

        if "jarvis" not in cmd:
            continue

        cmd = cmd.replace("jarvis", "").strip()
        speak("Yes boss?")

        if not cmd:
            set_status("LISTENING...")
            cmd = listen()

        if not cmd:
            continue

        set_status("PROCESSING...")
        # Fast commands
        if "open chrome" in cmd:
            speak("Opening Chrome")
            set_status("EXECUTING: OPEN CHROME")
            execute([{"cmd":"OPEN_CHROME"}])
            time.sleep(1)
            continue

        if "search google" in cmd:
            query = cmd.replace("search google", "")
            speak("Searching Google")
            set_status("EXECUTING: SEARCH GOOGLE")
            execute([{"cmd":"SEARCH_GOOGLE","arg":query}])
            time.sleep(1)
            continue

        set_status("THINKING...")
        p = plan(cmd)

        set_status("EXECUTING PLAN...")
        execute(p)
        time.sleep(1)
        set_status("READY")

if __name__ == "__main__":
    start_ui(run)
