import json

def load_settings():
    try:
        return json.load(open("settings.json"))
    except:
        return {"snake_color":[0,255,0],"grid":True,"sound":True}

def save_settings(s):
    json.dump(s, open("settings.json","w"))
