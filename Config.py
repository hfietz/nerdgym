#!/usr/bin/python
# vim: set fileencoding=utf-8 :

class Config:
    dir = '.'

    def __init__(self, dir):
        self.dir = dir
        print dir

    def getServerHost(self):
        return ''

    def getServerPort(self):
        return 8001

    def getDbPath(self):
        return 'db.sqlite'

    def getDocumentRoot(self):
        return self.dir + '/www'
