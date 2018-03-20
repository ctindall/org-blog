from flask import Flask,redirect,abort,send_from_directory,safe_join
import json
import os

#our stuff
from .Config import *
from .Collection import CollectionManager

class OrgBlogApp:
    
    def __init__(self):
        config = Config.read()
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
                return self.__collection_manager.get_all_collections(format="html")

        @self.__flask.route("/<string:collection_slug>/", methods=["GET"])
        @self.__flask.route("/<string:collection_slug>", methods=["GET"])
#        @self.__route("/<string:collection_slug>", methods=["GET"])
        def route_get_items(collection_slug):
            try:
                html = self.__collection_manager.get_all_collection_items(collection_slug, format="html")
                return html
            except LookupError:
                abort(404)
                
                
        @self.__flask.route("/<string:collection_slug>/<string:item_slug>", methods=["GET"])
        def route_get_item(collection_slug, item_slug):
            try:
                html = self.__collection_manager.get_collection_item(collection_slug, item_slug, format="html")
                return html
            except LookupError:
                abort(404)

        @self.__flask.route("/<string:collection_slug>/tag/<string:tag_slug>", methods=["GET"])
        def route_get_items_with_tag(collection_slug, tag_slug):
            try:
                html = self.__collection_manager.get_all_collection_items_with_tag(collection_slug, tag_slug, format="html")
                return html
            except LookupError:
                abort(404)

    def run(self):
        config = Config.read()
        self.__flask.run(host=config['host'], port=int(config['port']))

    def generate(self):
        pwd = os.path.dirname(os.path.abspath(__file__))
        print("generating static site into '{0}'".format(os.path.join(pwd, "_site/")))
