from voice import listen
from ai import plan
from executor import execute
from ui import start_ui
from speak import speak
import time

def run(set_status, add_log):
    set_status("SYSTEM READY")
    add_log("Boot sequence complete.")
    add_log("Waiting for trigger word 'Jarvis'.")

    while True:
        set_status("AWAITING COMMAND...")
        cmd = listen()

        if not cmd:
            continue

        if "jarvis" not in cmd:
            continue

        cmd = cmd.replace("jarvis", "").strip()
        speak("Yes boss?")
        add_log("Trigger recognized.")

        if not cmd:
            set_status("LISTENING...")
            add_log("Microphone active...")
            cmd = listen()

        if not cmd:
            add_log("No input detected.")
            continue

        add_log(f"User: {cmd}")
        set_status("PROCESSING...")

        # Fast commands bypassing AI
        if "open chrome" in cmd:
            speak("Opening Chrome")
            set_status("EXECUTING: CHROME")
            add_log("Action: OPEN_CHROME")
            execute([{"cmd":"OPEN_CHROME"}])
            time.sleep(1)
            continue

        if "search google" in cmd:
            query = cmd.replace("search google", "")
            speak("Searching Google")
            set_status("EXECUTING: SEARCH")
            add_log(f"Action: SEARCH_GOOGLE ({query})")
            execute([{"cmd":"SEARCH_GOOGLE","arg":query}])
            time.sleep(1)
            continue

        set_status("THINKING...")
        add_log("Consulting AI model...")
        p = plan(cmd)

        set_status("EXECUTING PLAN...")
        for step in p:
            add_log(f"Exec: {step.get('cmd')} {step.get('arg', '')}")

        execute(p)
        time.sleep(1)
        set_status("SYSTEM READY")

if __name__ == "__main__":
    start_ui(run)
