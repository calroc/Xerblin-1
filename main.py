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
import os, json
from types import FunctionType
from flask import Flask, render_template, Response, request
from xerblin import World, items


W = World()


WEBFACTION_TEMPLATES = '/home/calroc/webapps/smlaum/templates'


if os.path.exists(WEBFACTION_TEMPLATES):
  app = Flask(__name__, template_folder=WEBFACTION_TEMPLATES)
else:
  app = Flask(__name__)
  app.debug = True


@app.route("/")
def x():
  return render_template('index.html')


@app.route("/foo")
def foo():
  return render_template('inbrowser.html')


def _p(n):
  '''Convert functions into JSON representations.'''
  if isinstance(n, FunctionType):
    return {
      'class': '__function__',
      'name': n.__name__,
      }


def as_json(w):
  '''
  Return the current state of the World object w as a JSON string.
  Functions are converted to JS objects containing the functions' names.
  '''
  stack, dictionary = w.getCurrentState()
  dictionary = list(name for name, function in items(dictionary))
  return json.dumps((stack, dictionary), default=_p, indent=2)


def get_session(request):
  '''
  Return the World object for the request's session.
  (This is currently a stub that just returns the module
  global World.)
  '''
  return W


@app.route("/step", methods=['POST'])
def step():
  command = request.form['command']
  w = get_session(request)
  w.step(command.split())
  res = as_json(w)
  return Response(
    response='{"result":%s}' % (res,),
    mimetype='application/json',
    )


if __name__ == "__main__":
  app.run(debug=True)
