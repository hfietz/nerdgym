#!/usr/bin/python
# vim: set fileencoding=utf-8 :
import os
import re
from urllib import unquote

from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

class Server(HTTPServer):
    app = None
    cfg = None

    def __init__(self, app, cfg):
        self.app = app
        self.cfg = cfg
        HTTPServer.__init__(self, (cfg.getServerHost(), cfg.getServerPort()), Dispatcher)

    def hasRoute(self, path):
        for pattern, handler in self.app.routing().iteritems():
            if re.compile(pattern).match(path):
                return True
        return False

    def getRoute(self, path):
        for pattern, handler in self.app.routing().iteritems():
            match = re.compile(pattern).match(path)
            if match:
                return (handler, match.groups())
        return ()
    
    def getDocumentRoot(self):
        return self.cfg.getDocumentRoot()

class Dispatcher(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            (path, params) = self.parseQueryString(self.path)
            return self.processRequest(path, params)
        except Exception, e:
            self.renderError(e)
            return False

    def do_POST(self):
        try:
            (path, params) = self.parseQueryString(self.path)
            (mime, body) = self.readBody()
            if 'application/x-www-form-urlencoded' == mime:
                params.update(self.parseUrlencodedParams(body))
            return self.processRequest(path, params)
        except Exception, e:
            self.renderError(e)
            return False

    def processRequest(self, path, params):
        try:
            if self.isStaticFile(path):
                (mimeType, response) = self.readFile(path)
            elif self.server.hasRoute(path):
                (method, vars) = self.server.getRoute(path)
                (mimeType, response) = method(vars, params)
            else:
                raise NotFoundException(path)
            self.renderResponse(mimeType, response)
        except Exception, e:
            self.renderError(e)
        return True
    
    def parseQueryString(self, rawPath):
        rg = rawPath.split('?')
        path = rg[0]
        params = {}
        if (len(rg) > 1):
            params.update(self.parseUrlencodedParams(rg[1]))
        return (path, params)
    
    def readBody(self):
        mime = self.headers.gettype()
        len = int(self.headers.get('Content-length'))
        content = self.rfile.read(len)
        return (mime, content)

    def parseUrlencodedParams(self, s):
        params = {}
        if len(s) > 1:
            for var in s.split('&'):
                if '=' in var:
                    (k, v) = var.split('=')
                    params[unicode(unquote(k))] = unicode(unquote(v))
        return params

    def fileFromLocation(self, path):
        docroot = self.server.getDocumentRoot()
        path = docroot + '/' + path
        path = os.path.normpath(path)
        return path

    def isStaticFile(self, path):
        path = self.fileFromLocation(path)
        docroot = self.server.getDocumentRoot()
        if not path.startswith(docroot):
            raise AccessDeniedException(path)
        return os.path.isfile(path)

    def readFile(self, path):
        path = self.fileFromLocation(path)
        mime = SimpleHTTPRequestHandler.extensions_map[os.path.splitext(path)[1]]
        fp = open(path, 'rb')
        content = fp.read()
        fp.close()
        return (mime, content)

    def getParams(self):
        return {}

    def renderResponse(self, mimeType, response):
        self.send_response(200)
        self.send_header('Content-Type', mimeType)
        self.finishHeadersAndSendBody(response)

    def renderError(self, e):
        if isinstance(e, NotFoundException):
            status = 404
        elif isinstance(e, AccessDeniedException):
            status = 403
        else:
            status = 500
        self.send_response(status)
        s = "Fehler ('%s')" % e
        self.finishHeadersAndSendBody(s)

    def finishHeadersAndSendBody(self, body = ""):
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

class NotFoundException(Exception):
    path = ''

    def __init__(self, path):
        self.path = path
        Exception.__init__(self)

class AccessDeniedException(Exception):
    path = ''

    def __init__(self, path):
        self.path = path
        Exception.__init__(self)
