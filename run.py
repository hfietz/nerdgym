#!/usr/bin/python
# vim: set fileencoding=utf-8 :
import os
import sys

from BaseHTTPServer import HTTPServer

from Server import Server
from Config import Config
from App import App

cfg = Config(os.path.dirname(os.path.abspath(sys.argv[0])))
app = App(cfg)

server = Server(app, cfg)
try:
    server.serve_forever()
except KeyboardInterrupt:
    print "Goodbye."
