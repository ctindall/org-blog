from Org import OrgParser

import pystache
import re
import os

class Blog:
    def __init__(self, config):
        self.orgfile_path = config['entries_file']
        self.template_directory = config['template_directory']

    def __slugify(self, slug):
        slug = re.sub(r"[^\w\s-]", '', slug)#remove weird characters
        slug = re.sub(r"\s+", '-', slug)#condense whitespace down to dashes
        slug = slug.lower()
        return slug

    def __updateContext(self):
        self.context = {}
        self.context['entries'] = []

        op = OrgParser()
        entries = op.load(self.orgfile_path)
        for e in entries:
            entry = {}
            entry['title'] = e.get_title()
            entry['slug'] = self.__slugify(entry['title'])
            entry['html'] = e.to_html()
            self.context['entries'].append(entry)
    
    def getEntries(self, format="none"):
        self.__updateContext()
        
        if(format == "html"):
            template = open(os.path.join(self.template_directory, "entries.html"), "r").read()
            return pystache.render(template, self.context)
            
        else:
            return self.context['entries']

        
    def getEntry(self, slug, format="none"):
        self.__updateContext()

        for e in self.context['entries']:
            if e['slug'] == slug:
                entry = e
        
        if(format == "html"):
            template = open(os.path.join(self.template_directory, "entry.html"), "r").read()
            return pystache.render(template, entry)
        else:
            return entry
