#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Copyright © 2012, 2013 Simon Forman
#
#    This file is part of Xerblin
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
'''
Run a WSGI server with a World that stores its history in the git repo.
'''
from pickle import Unpickler
from os import getcwd
import logging
import sys
from xerblin import World
from gitty import CommitWorldMixin, make_commit_thing
import wsgiable


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


SYSTEM_PICKLE = 'system.pickle'


class CommitWorld(CommitWorldMixin, World, object):
    pass


try:
  with open(SYSTEM_PICKLE) as f:
    up = Unpickler(f)
    # Pull out all the sequentially saved state, command, state, ... data.
    # This loop will break after the last saved state is loaded leaving
    # the last saved state in the 'state' variable
    while True:
      try:
        state = up.load()
      except EOFError:
        break
except IOError, e:
  print e
  sys.exit(e.errno)


# Create a commit_thing to let us save our state to the git repo after
# changes.
try:
  commit_thing = make_commit_thing(getcwd(), [SYSTEM_PICKLE])
except ValueError, e:
  print e
  sys.exit(2)


w = CommitWorld(
  initial=state,
  save_file=SYSTEM_PICKLE,
  commit_thing=commit_thing,
  )


wsgiable.W = w
print "Serving on http://localhost:8000/ ..."
wsgiable.run()

