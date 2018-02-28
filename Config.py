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
            "collections_directory": "/var/org-blog/collections/",
            "template_directory": "/var/org-blog/templates/"
        }
    
        
    
    
