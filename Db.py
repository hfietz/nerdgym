#!/usr/bin/python
# vim: set fileencoding=utf-8 :
import sqlite3

class Db:
    connection = None

    def connect(self, filename):
        self.connection = sqlite3.connect(filename)
