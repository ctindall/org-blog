from flask import Flask,redirect,abort,send_from_directory,safe_join
import json
import os
import re

#our stuff
from .Config import *
from .Collection import CollectionManager

class OrgBlogApp:
    
    def __init__(self, config=Config.read()):
        self.__config = config
        self.__flask = Flask(__name__,
                           static_folder=Config.lookup("static_directory"),
                           static_url_path="/static")

        self.__collection_manager = CollectionManager(config)
        
        @self.__flask.route("/", methods=["GET"])
        def route_root():
            index_template = os.path.join(Config.lookup("template_directory"), "index.html")
            
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
        config = Config.read()
        self.__flask.run(host=self.__config['host'], port=int(self.__config['port']))

    def generate(self):
        dest = os.path.expanduser(self.__config["static_directory"])
        print("generating static site into '{0}'".format(dest))
        
        #index page
        if not os.path.exists(dest):
            os.mamekdirs(dest)
            
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
                with open(os.path.join(tag_directory, tag + ".html") as f:
                    f.write(self

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
        return self.self.__collection_manager.get_all_collection_items_with_tag(collection_slug, tag_slug, format=format)
