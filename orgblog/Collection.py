from .Org import OrgParser

import pystache
import re
import os

class CollectionManager():

    def __init__(self, config):
        self.__collections_directory = config['collections_directory']
        self.__template_directory = config['template_directory']
        
        self.__collections = [];
        
        #find all the relevant collections in the collections directory
        for f in os.scandir(self.__collections_directory):

            #create a Collection object for each relevant file and append it to our list
            match = re.search('^([^\#.]+)(\.org)$', os.path.basename(f.name))
            if match:
                slug = match.group(1)
                collection = Collection(slug, config)
                self.__collections.append(collection)

    def __update_context(self):
        self.__context = {}
        for collection in self.__collections:
            self.__context[collection.get_slug()] = collection.get_items()
        
    def get_slugs(self):
        return list(map(self.get_all_collections(),
                        lambda col: col.get_slug()))
    
    def get_all_collections(self, format=None):
        self.__update_context()
        
        if not format:
            return self.__collections

        if format == "html":
            template = open(os.path.join(self.__template_directory, "index.html"), "r").read()
            return pystache.render(template, self.__context)
        
        else:
            return self.__context

    def __items_template_exists(self, collection_slug):
        template_path = os.path.join(self.__template_directory, collection_slug, "items.html")
        return os.path.exists(template_path)
        
    def get_all_collection_items(self, collection_slug, format=None):
        
        if format == "html" and not self.__items_template_exists(collection_slug):
            raise LookupError("There is no items.html template for the collection '" + collection_slug + "'")
        
        for c in self.get_all_collections():
            if c.get_slug() == collection_slug:
                return c.get_items(format=format)
            
        raise LookupError("The collection '" + collection_slug + "' does not exist")

    def __item_template_exists(self, collection_slug):
        template_path = os.path.join(self.__template_directory, collection_slug, "item.html")
        return os.path.exists(template_path)
    
    def get_collection_item(self, collection_slug, item_slug, format=None):
        if format == "html" and not self.__item_template_exists(collection_slug):
            raise LookupError("There is no item.html template for the collection '" + collection_slug + "'")
        
        for c in self.get_all_collections():
            if c.get_slug() == collection_slug:
                return c.get_item(item_slug, format=format)

    def __tag_template_exists(self, collection_slug):
        template_path = os.path.join(self.__template_directory, collection_slug, "tag.html")
        return os.path.exists(template_path)

    def get_all_collection_items_with_tag(self, collection_slug, tag_slug, format=None):
        if format == "html" and not self.__tag_template_exists(collection_slug):
            raise LookupError("There is no tag.html template for the collection '" + collection_slug + "'")

        for c in self.get_all_collections():
            if c.get_slug() == collection_slug:
                return c.get_items_with_tag(tag_slug, format=format)
            
        raise LookupError("The collection '" + collection_slug + "' does not exist")
       
        
class Collection:
    
    def __init__(self, collection_slug, config):
        self.__orgfile_path = os.path.join(config['collections_directory'], collection_slug + ".org")
        self.__template_directory = config['template_directory']
        self.__collection_slug = collection_slug

    def __slugify(self, slug):
        slug = re.sub(r"[^\w\s-]", '', slug)#remove weird characters
        slug = re.sub(r"\s+", '-', slug)#condense whitespace down to dashes
        slug = slug.lower()
        return slug

    def __updateContext(self):
        self.context = {}
        self.context['items'] = []

        op = OrgParser()
        items = op.load(self.__orgfile_path)
        for i in items:
            item = {}
            item['title'] = i.get_title()
            item['slug'] = self.__slugify(item['title'])
            item['html'] = i.to_html()
            item['tags'] = i.get_tags()
            
            self.context['items'].append(item)
    
    def get_items(self, format=None):
        self.__updateContext()
        
        if(format == "html"):
            template = open(os.path.join(self.__template_directory, self.__collection_slug, "items.html"), "r").read()
            return pystache.render(template, self.context)
            
        else:
            return self.context['items']
        
    def get_item(self, slug, format=None):
        self.__updateContext()
        item = None
        
        for i in self.context['items']:
            if i['slug'] == slug:
                item = i

        if not item:
            raise LookupError("The item '" + slug + "' does not exist in the collection '" + self.__collection_slug + "'")
        
        if(format == "html"):
            template = open(os.path.join(self.__template_directory, self.__collection_slug, "item.html"), "r").read()
            return pystache.render(template, item)
        else:
            return item

    def get_items_with_tag(self, tag, format=None):
        self.__updateContext()
        items = []
        
        for i in self.context['items']:
            if tag in i['tags']:
                items.append(i)

        context = {}
        context['tag'] = tag
        context['items'] = items
        
        if(format == "html"):
            template = open(os.path.join(self.__template_directory, self.__collection_slug, "tag.html"), "r").read()
            return pystache.render(template, context)
        else:
            return items

        
    def get_slug(self):
        return self.__collection_slug
