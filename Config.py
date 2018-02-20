import json
import os

def read():
    if(os.path.isfile(os.path.expanduser("~/.org-blog.json"))):
        return json.loads(open(os.path.expanduser("~/.org-blog.json")).read())
    elif(os.path.isfile("/etc/org-blog.json")):
        return json.loads(open(os.path.expanduser("/etc/org-blog.json")).read())
    else:
        #if all else fails, use default values
        return { 
            "entries_file": "/var/org-blog/entries.org",
            "template_directory": "/var/org-blog/templates/"
        }
    
        
    
    
