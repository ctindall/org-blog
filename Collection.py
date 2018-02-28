from Org import OrgParser

import pystache
import re
import os

class Collection:
    def __init__(self, collection_slug, config):
        self.orgfile_path = os.path.join(config['collections_directory'], collection_slug + ".org")
        self.template_directory = config['template_directory']
        self.collection_slug = collection_slug

    def __slugify(self, slug):
        slug = re.sub(r"[^\w\s-]", '', slug)#remove weird characters
        slug = re.sub(r"\s+", '-', slug)#condense whitespace down to dashes
        slug = slug.lower()
        return slug

    def __updateContext(self):
        self.context = {}
        self.context['items'] = []

        op = OrgParser()
        items = op.load(self.orgfile_path)
        for i in items:
            item = {}
            item['title'] = i.get_title()
            item['slug'] = self.__slugify(item['title'])
            item['html'] = i.to_html()
            self.context['items'].append(item)
    
    def get_items(self, format="none"):
        self.__updateContext()
        
        if(format == "html"):
            template = open(os.path.join(self.template_directory, self.collection_slug, "items.html"), "r").read()
            return pystache.render(template, self.context)
            
        else:
            return self.context['items']

        
    def get_item(self, slug, format="none"):
        self.__updateContext()

        for i in self.context['items']:
            if i['slug'] == slug:
                item = i
        
        if(format == "html"):
            template = open(os.path.join(self.template_directory, self.collection_slug, "item.html"), "r").read()
            return pystache.render(template, item)
        else:
            return item
