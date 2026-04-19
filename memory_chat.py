import json, os

FILE = "chat_history.json"
MAX_TURNS = 6

def load_history():
    if not os.path.exists(FILE):
        return []
    return json.load(open(FILE))

def save_history(history):
    history = history[-MAX_TURNS:]
    json.dump(history, open(FILE, "w"), indent=2)

def add_turn(user, assistant):
    hist = load_history()
    hist.append({"user": user, "assistant": assistant})
    save_history(hist)

def build_context():
    hist = load_history()
    context = ""
    for h in hist:
        context += f"User: {h['user']}\nAssistant: {h['assistant']}\n"
    return context
