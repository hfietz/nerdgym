#!/usr/bin/python
# vim: set fileencoding=utf-8 :
import os
import sys

from Server import Server
from Config import Config
from Nerdgym import Nerdgym

cfg = Config(os.path.dirname(os.path.abspath(sys.argv[0])))
app = Nerdgym(cfg)

server = Server(app, cfg)
try:
    server.serve_forever()
except KeyboardInterrupt:
    print "Goodbye."
