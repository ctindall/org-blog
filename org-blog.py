#!/usr/bin/env python3

from flask import Flask,redirect
import json

#our stuff
from Collection import Collection
import Config

app = Flask(__name__)
config = Config.read()

@app.route("/<string:collection_slug>/", methods=["GET"])
@app.route("/<string:collection_slug>", methods=["GET"])
def route_get_items(collection_slug):
    collection = Collection(collection_slug, config)
    return collection.get_items(format="html")

@app.route("/<string:collection_slug>/<string:item_slug>", methods=["GET"])
def route_get_item(collection_slug, item_slug):
    collection = Collection(collection_slug, config)
    return collection.get_item(item_slug, format="html")
