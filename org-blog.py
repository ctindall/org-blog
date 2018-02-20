#!/usr/bin/env python3

from flask import Flask
import json

#our stuff
from Blog import Blog
import Config

app = Flask(__name__)
config = Config.read()
blog = Blog(config)

@app.route("/entries/", methods=["GET"])
@app.route("/entries", methods=["GET"])
def route_get_entry():
    return blog.getEntries(format="html")

@app.route("/entries/<string:slug>", methods=["GET"])
def route_get_entries(slug):
    return blog.getEntry(slug, format="html")
