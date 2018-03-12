import json
import os

defaults = { 
    "collections_directory": "~/.orgblog/collections/",
    "template_directory": "~/.orgblog/templates/",
    "host": "127.0.0.1",
    "port": "5000"
}

def read():
    config = {}
    
    if os.path.isfile(os.path.expanduser("~/.orgblog.json")):
        config = json.loads(open(os.path.expanduser("~/.orgblog.json")).read())
    elif os.path.isfile("/etc/orgblog.json"):
        config = json.loads(open(os.path.expanduser("/etc/orgblog.json")).read())
    else:
        config = defaults

    for key in defaults:
        if not key in config:
            config[key] = defaults[key]

        if key.endswith("_directory"):
            config[key] = os.path.expanduser(config[key])
            
    return config
    
    
def install_default(silent=False):
    
    if os.path.isdir(os.path.expanduser("~/")):
        conf_file = open(os.path.expanduser("~/.orgblog.json"), "w")
    else:
        return False

    try:
        if not silent:
            print("Installing default config to ~/.orgblog.json")

        json.dump(defaults, conf_file)
        conf_file.close()
        return True
    
    except FileNotFoundEror:
        return False

def lookup(key):
    config = read()
    return config[key]
    
