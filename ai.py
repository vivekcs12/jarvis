import requests, json
from memory_chat import build_context, add_turn

CACHE = {}

def plan(command):
    if command in CACHE:
        return CACHE[command]

    context = build_context()

    prompt = f'''
Return ONLY JSON array.
Max 3 steps.

Context:
{context}

User: {command}
'''

    res = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "gemma:2b-instruct-q4_0", "prompt": prompt, "stream": False}
    )

    text = res.json()["response"]

    try:
        start = text.find("[")
        end = text.rfind("]") + 1
        result = json.loads(text[start:end])
    except:
        result = []

    add_turn(command, text)
    CACHE[command] = result
    return result
