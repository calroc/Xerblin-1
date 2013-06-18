#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Copyright © 2013 Simon Forman
#
#    This file is part of Xerblin.
#
#    Xerblin is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Xerblin is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Xerblin.  If not, see <http://www.gnu.org/licenses/>.
#
from sys import stderr
from traceback import format_exc
from types import FunctionType
from os.path import exists
from urlparse import parse_qs
from wsgiref.simple_server import make_server
from templates import render
from xerblin import World, items


W = World()


def get_session(environ):
  '''
  Return the World object for the request's session.
  (This is currently a stub that just returns the module
  global World.)
  '''
  return W


def get_form_values(environ):
  size = int(environ.get('CONTENT_LENGTH') or 0)
  data = environ['wsgi.input'].read(size)
  return parse_qs(data)


def step(command, environ):
  w = get_session(environ)
  w.step(command.split())


def x(environ, start_response):
  path = environ['PATH_INFO'].lstrip('/').split('/', 1)

  if path == ['']: # Root
    try:
      I = get_session(environ).getCurrentState()
    except:
      start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
      return [format_exc()]
    start_response('200 OK', [('Content-type', 'text/html')])
    return render(I)

  if path == ['foo']:
    start_response('200 OK', [('Content-type', 'text/html')])
    return open('templates/inbrowser.html')

  if path == ['step']:
    form_data = get_form_values(environ)
    command = form_data.get('command', [''])[0]
    try:
      step(command, environ)
    except:
      start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
      return [format_exc()]

    start_response('301 Redirect', [('Location', '/'),])
    return []

  if len(path) == 2 and path[0] == 'static':
    fn = environ['PATH_INFO'].lstrip('/')
    if exists(fn):
      if fn.endswith('.css'):
        mime_type = 'text/css'
      else:
        raise ValueError("We don't server your kind around here! %r" % (fn,))
    start_response('200 OK', [('Content-type', mime_type)])
    return open(fn)
 
  print >> stderr, path
  start_response('501 Not Implemented', [('Content-type', 'text/plain')])
  return ["D'oh! 501 Not Implemented ", repr(environ['PATH_INFO'])]


def run(app=x, host='', port=8000):
  httpd = make_server(host, port, app)
  httpd.serve_forever()


if __name__ == '__main__':
  print "Serving on port 8000..."
  run()
