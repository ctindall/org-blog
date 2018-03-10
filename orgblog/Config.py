import json
import os

def read():
    if(os.path.isfile(os.path.expanduser("~/.orgblog.json"))):
        return json.loads(open(os.path.expanduser("~/.orgblog.json")).read())
    elif(os.path.isfile("/etc/orgblog.json")):
        return json.loads(open(os.path.expanduser("/etc/orgblog.json")).read())
    else:
        #if all else fails, use default values
        return { 
            "collections_directory": "/var/org-blog/collections/",
            "template_directory": "/var/org-blog/templates/",
            "host": "0.0.0.0",
            "port": "5000",
        }
    
        
    
    
