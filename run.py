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
from traceback import format_exc
from urlparse import parse_qs
from wsgiref.simple_server import make_server
from gitty import WorldCache
from html import render, commit_list


cache = WorldCache()
CSS = open('./static/site.css').read()


def start(start_response, message, mime_type):
  start_response(message, [('Content-type', mime_type)])


def err500(start_response, message):
  start(start_response, '500 Internal Server Error', 'text/plain')
  return [str(message)]


def ok200(start_response, response, mimetype='text/html'):
  start(start_response, '200 OK', mimetype)
  return response


def report_problems(f):
  def inner(environ, start_response):
    try:
      return f(environ, start_response)
    except:
      return err500(start_response, format_exc())
  return inner


def parse_post(environ):
  try:
    request_body_size = int(environ.get('CONTENT_LENGTH', 0))
  except ValueError:
    request_body_size = 0
  request_body = environ['wsgi.input'].read(request_body_size)
  return parse_qs(request_body)['command'][0]


@report_problems
def x(environ, start_response):
  path = environ['PATH_INFO'].lstrip('/').split('/', 1)

  if path == ['']: # Root
    return ok200(start_response, commit_list(cache.commit_list()))

  if path == ['static', 'site.css']:
    return ok200(start_response, CSS, 'text/css')

  sha = path[0]
  if len(sha) != 40:
    raise ValueError('incorrect length %r' % (sha,))
  if not sha.isalnum():
    raise ValueError('invalid %r' % (sha,))

  if len(path) == 1: # Just render the state.
    I = cache.get_interpreter_from_sha(sha)
    return ok200(start_response, render(I, sha))

  command = path[1]
  if not command.replace('_', '').isalnum():
    raise ValueError('invalid %r' % (command,))

  if command == 'interpret':
    command = parse_post(environ).split()
  else:
    command = [command]

  new_sha = cache.step(sha, command)

  start_response('301 Redirect', [('Location', '/' + new_sha)])
  return []


def run(app=x, host='', port=8000):
  httpd = make_server(host, port, app)
  httpd.serve_forever()


if __name__ == '__main__':
  print len(cache.cache), 'previous states'
  print "Serving on port http://localhost:8000/ ..."
  run()
