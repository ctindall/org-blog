from flask import Flask,redirect,abort
import json
import os

#our stuff
from .Config import *
from .Collection import CollectionManager

class OrgBlogApp:
    def __init__(self):
        self.__app = Flask(__name__)
        config = Config.read()

        @self.__app.route("/", methods=["GET"])
        def route_root():
            index_template = os.path.join(Config.lookup("template_directory"), "index.html")
            
            if not os.path.exists(index_template) or not os.path.isfile(index_template):
                abort(404)
            else:
                collection_manager = CollectionManager(config)
                return collection_manager.get_all_collections(format="html")

        @self.__app.route("/<string:collection_slug>/", methods=["GET"])
        @self.__app.route("/<string:collection_slug>", methods=["GET"])
        def route_get_items(collection_slug):
            collection_manager = CollectionManager(config)
            try:
                html = collection_manager.get_all_collection_items(collection_slug, format="html")
                return html
            except LookupError:
                abort(404)
                
                
        @self.__app.route("/<string:collection_slug>/<string:item_slug>", methods=["GET"])
        def route_get_item(collection_slug, item_slug):
            collection_manager = CollectionManager(config)
            try:
                html = collection_manager.get_collection_item(collection_slug, item_slug, format="html")
                return html
            except LookupError:
                abort(404)

        @self.__app.route("/<string:collection_slug>/tag/<string:tag_slug>", methods=["GET"])
        def route_get_items_with_tag(collection_slug, tag_slug):
            collection_manager = CollectionManager(config)
            try:
                html = collection_manager.get_all_collection_items_with_tag(collection_slug, tag_slug, format="html")
                return html
            except LookupError:
                abort(404)

    def run(self):
        config = Config.read()
        self.__app.run(host=config['host'], port=int(config['port']))
