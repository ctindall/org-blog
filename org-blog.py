#!/usr/bin/env python3

from flask import Flask,redirect,abort
import json

#our stuff
import Config
from Collection import CollectionManager

app = Flask(__name__)
config = Config.read()

@app.route("/", methods=["GET"])
def route_root():
    collection_manager = CollectionManager(config)
    return collection_manager.get_all_collections(format="html")

@app.route("/<string:collection_slug>/", methods=["GET"])
@app.route("/<string:collection_slug>", methods=["GET"])
def route_get_items(collection_slug):
    collection_manager = CollectionManager(config)
    try:
        html = collection_manager.get_all_collection_items(collection_slug, format="html")
        return html
    except LookupError:
        abort(404)
    

@app.route("/<string:collection_slug>/<string:item_slug>", methods=["GET"])
def route_get_item(collection_slug, item_slug):
    collection_manager = CollectionManager(config)
    try:
        html = collection_manager.get_collection_item(collection_slug, item_slug, format="html")
        return html
    except LookupError:
        abort(404)

@app.route("/<string:collection_slug>/tag/<string:tag_slug>", methods=["GET"])
def route_get_items_with_tag(collection_slug, tag_slug):
    collection_manager = CollectionManager(config)
    try:
        html = collection_manager.get_all_collection_items_with_tag(collection_slug, tag_slug, format="html")
        return html
    except LookupError:
        abort(404)
