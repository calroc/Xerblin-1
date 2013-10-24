#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Copyright © 2013 Simon Forman
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
from os.path import join
from operator import attrgetter
from pickle import Unpickler, dump
from StringIO import StringIO
import sys
sys.path.insert(0, './dulwich-0.9.0.zip/dulwich-0.9.0')
from dulwich.repo import Repo
from xerblin import interpret


pickle_name='system.pickle'
sort_key = attrgetter('commit_time')


def load_latest_state(data):
  load = Unpickler(StringIO(data)).load
  state = None
  while True:
    try:
      state = load()
    except EOFError:
      break
  return state


class WorldCache(object):

  cache = {} # SHAs to interpreters
  reverse_cache = {} # Interpreters to SHAs
  _mode = 0100644

  def __init__(self, path='.'):
    self.path = path
    self.repo = repo = Repo(path)
    H = [
      commit
      for commit in repo.revision_history(repo.head())
      if pickle_name in repo[commit.tree]
      ]
    H.sort(key=sort_key)
    for commit in H:
      I = load_latest_state(repo[repo[commit.tree][pickle_name][1]].data)

      try: seen_sha = self.reverse_cache[I]
      except KeyError: pass
      else: I = self.cache[seen_sha] # reuse the seen interpreter to save memory.

      self.cache[commit.id] = I
      self.reverse_cache[I] = commit.id

  def get_interpreter_from_sha(self, sha):
    return self.cache[sha]

  def commit_list(self):
    return self.cache.keys()

  def step(self, sha, command):
    I = self.get_interpreter_from_sha(sha)
    new_I = interpret(I, command)
    new_sha = self.check_for_prev_I(new_I, sha)
    return new_sha

  def check_for_prev_I(self, I, sha):
    try:
      new_sha = self.reverse_cache[I]
    except KeyError:
      new_sha = self.commit_new(I, sha)
      self.reverse_cache[I] = new_sha
      self.cache[new_sha] = I
    return new_sha

  def commit_new(self, I, sha):
    with open(join(self.path, pickle_name), 'wb') as pickly:
      dump(I, pickly)
    self.repo.stage([pickle_name])
    commit_sha = self.repo.do_commit('autosave from %r' % (sha,))
    print >> sys.stderr, "generating new commit", commit_sha
    return commit_sha
