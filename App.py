#!/usr/bin/python
# vim: set fileencoding=utf-8 :
from Db import Db

class App:
    user = None
    cfg = None
    db = None

    def __init__(self, cfg):
        self.cfg = cfg
        self.db = Db()
        if self.db:
            self.db.connect(cfg.getDbPath())
    
    def routing(self):
        return { 
            '/hello/([^/]+)/?': self.sayHello,
            '/(test)': self.sayHello
            }

    def sayHello(self, vars, params):
        s = '<h1>Hello, %s</h1>' % vars[0]
        s += "%s" % params
        return ('text/html', s)
