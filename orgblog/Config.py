import json
import os


class Config:

    def __init__(self, **kwargs):
        defaults = { 
            "collections_directory": "~/.orgblog/collections/",
            "template_directory": "~/.orgblog/templates/",
            "static_directory": "~/.orgblog/static/",
            "visible_todo_statuses": ["DONE"],
            "host": "127.0.0.1",
            "port": "5000"
        }
        
        self.__config = {}

        if 'filename' in kwargs.keys() and os.path.isfile(kwargs['filename']):
            self.__config = json.loads(open(kwargs['filename']).read())
        elif os.path.isfile(os.path.expanduser("~/.orgblog.json")):
            self.__config = json.loads(open(os.path.expanduser("~/.orgblog.json")).read())
        elif os.path.isfile("/etc/orgblog.json"):
            self.__config = json.loads(open("/etc/orgblog.json").read())
        else:
            self.__config = defaults

        for key in defaults:
            if not key in self.__config:
                self.__config[key] = defaults[key]

            if key.endswith("_directory"):
                self.__config[key] = os.path.expanduser(self.__config[key])


    def read(self):
        return self.__config

    def lookup(self, key):
        return self.__config[key]

    def install_default(self, silent=False):
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
