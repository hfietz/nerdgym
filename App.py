#!/usr/bin/python
# vim: set fileencoding=utf-8 :
import json

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
            '/hello/([^/]+)/?': self.echo,
            '/(test)': self.echo
            }

    def echo(self, vars, params):
        params[u'path_vars'] = vars
        return self.to_json_response(params)

    def to_json_response(self, data):
        s = json.dumps(data, indent=2)
        return ('text/json', s)
