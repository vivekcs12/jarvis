import requests, json
from memory_chat import build_context, add_turn

CACHE = {}

def plan(command):
    if command in CACHE:
        return CACHE[command]

    context = build_context()

    prompt = f'''
You are J.A.R.V.I.S., a highly advanced AI system designed to give your user complete, hands-free automation over their computer.
Your user is also an 11th-grade JEE aspirant, so you must provide brilliant, concise academic guidance if asked.

You must reply with a valid JSON array of action objects. Do not output anything else.

Available commands to control the computer:
- {{"cmd": "OPEN_APP", "arg": "app_name"}} (e.g. notepad, calc, chrome)
- {{"cmd": "SEARCH_GOOGLE", "arg": "query"}}
- {{"cmd": "TYPE", "arg": "text to type"}}
- {{"cmd": "PRESS", "arg": "enter"}} (or "tab", "esc", "win")
- {{"cmd": "HOTKEY", "arg": "ctrl,c"}} (e.g. "win,d" for desktop, "alt,tab")
- {{"cmd": "WAIT", "arg": "1.0"}}
- {{"cmd": "RUN_CMD", "arg": "terminal command"}}
- {{"cmd": "MOUSE_MOVE", "arg": "x,y"}}
- {{"cmd": "MOUSE_CLICK"}}
- {{"cmd": "SPEAK", "arg": "Spoken text"}}

Example - If user asks "Minimize everything and open notepad":
[
  {{"cmd": "HOTKEY", "arg": "win,d"}},
  {{"cmd": "WAIT", "arg": "0.5"}},
  {{"cmd": "RUN_CMD", "arg": "start notepad"}},
  {{"cmd": "SPEAK", "arg": "Minimizing windows and launching Notepad, sir."}}
]

Context of previous conversation:
{context}

User Command: {command}
'''

    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "gemma:2b", "prompt": prompt, "stream": False},
            timeout=10
        )

        text = res.json().get("response", "")

        try:
            start = text.find("[")
            end = text.rfind("]") + 1
            if start != -1 and end != 0:
                result = json.loads(text[start:end])
            else:
                result = [{"cmd": "SPEAK", "arg": "I did not generate a valid plan. " + text.replace('"', '').strip()}]
        except:
            result = [{"cmd": "SPEAK", "arg": "Error parsing plan."}]

    except Exception as e:
        print(f"LLM Error: {e}")
        result = [{"cmd": "SPEAK", "arg": f"Sir, I am unable to connect to the central AI server. Please check your Ollama instance."}]
        text = str(result)

    add_turn(command, text)
    CACHE[command] = result
    return result
