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
import logging
from os.path import join
from time import time
from pickle import Unpickler, dump
from StringIO import StringIO
import sys
sys.path.insert(0, './dulwich-0.9.0.zip/dulwich-0.9.0')
from dulwich.repo import Repo, NotGitRepository
from dulwich.objects import Blob, Tree, Commit, parse_timezone


class WorldCache(object):

  cache = {}
  _mode = 0100644

  def __init__(self, path='.'):
    self.path = path
    self.repo = Repo(path)
    self.commits = dict(
      (commit.id, commit)
      for commit in self.repo.revision_history(self.repo.head())
      )

  def commit_new(self, I, pickle_name='system.pickle'):
    with open(join(self.path, pickle_name), 'wb') as pickly:
      dump(I, pickly)
    self.repo.stage([pickle_name])
    commit_sha = self.repo.do_commit('autosave')
    self.cache[commit_sha, pickle_name] = I
    return commit_sha

  def commit_list(self):
    return self.commits.keys()

  def get_pickle_from_sha(self, sha, pickle_name='system.pickle'):
    try:
      commit = self.commits[sha]
    except KeyError:
      commit = self.commits[sha] = self.repo[sha]
    return self.get_pickle_from_commit(commit, pickle_name)

  def get_pickle_from_commit(self, commit, pickle_name='system.pickle'):
    key = commit.id, pickle_name
    try:
      return self.cache[key]
    except KeyError:
      pass
    print >> sys.stderr, 'cache miss', commit, pickle_name
    _, sha = self.repo[commit.tree][pickle_name] # mode is unused
    I = self.cache[key] = self.load_latest_state(self.repo[sha].data)
    return I

  def load_latest_state(self, data):
    load = Unpickler(StringIO(data)).load
    # Pull out all the sequentially saved state, command, state, ... data.
    # This loop will break after the last saved state is loaded leaving
    # the last saved state in the 'state' variable
    state = None
    while True:
      try:
        state = load()
      except EOFError:
        break
    return state


class CommitWorldMixin(object):

  def __init__(self, *a, **b):
    self.commit_thing = b.pop('commit_thing')
    super(CommitWorldMixin, self).__init__(*a, **b)

  def setCurrentState(self, state):
    super(CommitWorldMixin, self).setCurrentState(state)
    self.commit_thing()


def make_commit_thing(path, files):
  log = logging.getLogger('COMMIT')
  try:
    repo = Repo(path)
  except NotGitRepository:
    log.critical("%r isn't a repository!", path)
    raise ValueError("%r isn't a repository!" % (path,))

  # Note that we bind the args as defaults rather than via a closure so
  # you can override them later if you want.  (Technically, binding the
  # values as defaults IS a type of closure, but you know what I mean!)
  def commit(files=files, repo=repo, log=log):
    repo.stage(files)
    commit_sha = repo.do_commit('autosave')
    log.info('commit %s', commit_sha)

  return commit



##if __name__ == '__main__':
##  wc = WorldCache()
##  sha = wc.commit_list()[2]
##  I = wc.get_pickle_from_sha(sha)
##  ooo = wc.commit_new(I)
