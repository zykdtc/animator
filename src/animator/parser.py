import json

def load_instructions(path):
    with open(path, "r") as f:
        return json.load(f)
