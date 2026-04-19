import requests, json
from memory_chat import build_context, add_turn

CACHE = {}

def plan(command):
    if command in CACHE:
        return CACHE[command]

    context = build_context()

    prompt = f'''
You are J.A.R.V.I.S., a highly advanced, futuristic AI assistant.
Your current user is an ambitious 11th-grade JEE aspirant. You act as an elite study mentor (for Physics, Chemistry, Math) AND a system administrator capable of completely controlling their computer.

You must reply with a valid JSON array of action objects.
Return ONLY the JSON array. Do not output any markdown formatting, thoughts, or extra text.

Available commands:
- {{"cmd": "OPEN_CHROME"}}
- {{"cmd": "SEARCH_GOOGLE", "arg": "query"}}
- {{"cmd": "OPEN_APP", "arg": "app_name"}} (e.g. notepad, calc)
- {{"cmd": "TYPE", "arg": "text"}}
- {{"cmd": "PRESS", "arg": "enter"}}
- {{"cmd": "WAIT", "arg": "1.0"}}
- {{"cmd": "RUN_CMD", "arg": "terminal command"}}
- {{"cmd": "MOUSE_MOVE", "arg": "x,y"}}
- {{"cmd": "MOUSE_CLICK"}}
- {{"cmd": "SPEAK", "arg": "Your spoken response here"}}

If the user asks a question (like a JEE concept), explain it like a brilliant, strict but supportive mentor using the SPEAK command. Keep spoken answers concise but profound.
If the user asks you to do something on the computer, string together the right commands to accomplish it.

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

        # If ollama isn't running or the model isn't there, we handle it gracefully below
        text = res.json().get("response", "")

        try:
            start = text.find("[")
            end = text.rfind("]") + 1
            if start != -1 and end != 0:
                result = json.loads(text[start:end])
            else:
                # Fallback if no JSON array found
                result = [{"cmd": "SPEAK", "arg": "I did not generate a valid plan. " + text.replace('"', '').strip()}]
        except:
            result = [{"cmd": "SPEAK", "arg": "Error parsing plan."}]

    except Exception as e:
        # Fallback when the local LLM server is not running
        print(f"LLM Error: {e}")
        result = [{"cmd": "SPEAK", "arg": f"Sir, I am unable to connect to the central AI server. Please check your Ollama instance."}]
        text = str(result)

    add_turn(command, text)
    CACHE[command] = result
    return result
