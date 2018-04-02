from flask import Flask,redirect,abort,send_from_directory,safe_join
import json
import os
import re

#our stuff
from .Config import Config
from .Collection import CollectionManager

class OrgBlogApp:
    
    def __init__(self, config=Config()):
        self.__config = config
        self.__flask = Flask(__name__,
                           static_folder=self.__config.lookup("static_directory"),
                           static_url_path="/static")

        self.__collection_manager = CollectionManager(self.__config)
        
        @self.__flask.route("/", methods=["GET"])
        def route_root():
            index_template = os.path.join(self.__config.lookup("template_directory"), "index.html")
            
            if not os.path.exists(index_template) or not os.path.isfile(index_template):
                abort(404)
            else:
                return self.get_all_collections(format="html")

        @self.__flask.route("/<string:collection_slug>/", methods=["GET"])
        @self.__flask.route("/<string:collection_slug>", methods=["GET"])
        def route_get_items(collection_slug):
            try:
                html = self.get_all_collection_items(collection_slug, format="html")
                return html
            except LookupError:
                abort(404)
                
                
        @self.__flask.route("/<string:collection_slug>/<string:item_slug>", methods=["GET"])
        def route_get_item(collection_slug, item_slug):
            try:
                html = self.get_collection_item(collection_slug, item_slug, format="html")
                return html
            except LookupError:
                abort(404)

        @self.__flask.route("/<string:collection_slug>/tag/<string:tag_slug>", methods=["GET"])
        def route_get_items_with_tag(collection_slug, tag_slug):
            try:
                html = self.get_all_collection_items_with_tag(collection_slug, tag_slug, format="html")
                return html
            except LookupError:
                abort(404)        
                
    def run(self):
        self.__flask.run(host=self.__config.lookup('host'), port=int(self.__config.lookup('port')))

    def generate(self):
        dest = os.path.join(os.getcwd(), "_site")
        print("generating static site into '{0}'".format(dest))
        
        #index page
        if not os.path.exists(dest):
            os.makedirs(dest)
            
        with open(os.path.join(dest, "index.html"), "w") as f:
            f.write(self.get_all_collections(format="html"))

        for collection in self.get_all_collections():
            #collection index pages
            collection_directory = os.path.join(dest, collection.get_slug())
            if not os.path.exists(collection_directory):
                os.makedirs(collection_directory)
            with open(os.path.join(collection_directory, "index.html"), "w") as f:
                f.write(self.get_all_collection_items(collection.get_slug(), format="html"))

            #collection tag pages
            tag_directory = os.path.join(collection_directory, "tag")
            if not os.path.exists(tag_directory):
                os.makedirs(tag_directory)
            for tag in collection.get_tags():
                with open(os.path.join(tag_directory, tag + ".html"), "w") as f:
                    f.write(self.get_all_collection_items_with_tag(collection.get_slug(), tag, format="html"))

            #collection item pages
            for item in collection.get_items():
                with open(os.path.join(collection_directory, item['slug'] + ".html"), "w") as f:
                    f.write(self.get_collection_item(collection.get_slug(), item['slug'], format="html"))

    #CollectionManager convenience methods
    def get_slugs(self):
        return self.__collection_manager.get_slugs()

    def get_all_collections(self, *args, **kwargs):
        return self.__collection_manager.get_all_collections(**kwargs)

    def get_all_collection_items(self, collection_slug, *, format):
        return self.__collection_manager.get_all_collection_items(collection_slug, format=format)

    def get_collection_item(self, collection_slug, item_slug, *, format):
        return self.__collection_manager.get_collection_item(collection_slug, item_slug, format=format)

    def get_all_collection_items_with_tag(self, collection_slug, tag_slug, *, format):
        return self.__collection_manager.get_all_collection_items_with_tag(collection_slug, tag_slug, format=format)
