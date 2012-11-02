#!/usr/bin/python
# vim: set fileencoding=utf-8 :

from App import App

class Nerdgym(App):
    def routing(self):
        routes = App.routing(self)
        return routes