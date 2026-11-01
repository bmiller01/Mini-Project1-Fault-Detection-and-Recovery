import json
import os

filename = os.path.join(os.path.dirname(__file__), "checkpoint.json")
def save_state(state):
    #create/save temporary file 
    with open(filename + ".tmp", "w") as file:
        json.dump(state, file)
    os.replace(filename + ".tmp", filename)

def load_state():
    with open(filename, "r") as file:
        return json.load(file)
