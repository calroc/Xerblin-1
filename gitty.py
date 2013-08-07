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
from operator import attrgetter
from pickle import Unpickler, dump
from StringIO import StringIO
import sys
sys.path.insert(0, './dulwich-0.9.0.zip/dulwich-0.9.0')
from dulwich.repo import Repo, NotGitRepository
from dulwich.objects import Blob, Tree, Commit, parse_timezone
from xerblin import interpret


pickle_name='system.pickle'


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
    return self.commits.keys()

  def step(self, sha, command):
    I = self.get_interpreter_from_sha(sha)
    new_I = interpret(I, [command])
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


def process_commits(repo, sort_key=attrgetter('commit_time')):
  H = repo.revision_history(repo.head())
  H.sort(key=sort_key)
  for commit in H:
    tree = repo[commit.tree]
    try:
      blob_mode, blob_sha = tree[pickle_name]
    except KeyError:
      continue
    blob = repo[blob_sha]
    yield commit.id, load_latest_state(blob.data)


def load_map(path='.'):
  repo = Repo(path)
  I2SHA = {}
  for sha, I in process_commits(repo):
    try:
      seen_sha = I2SHA[I]
    except KeyError:
      I2SHA[I] = sha
    else:
      yield sha, seen_sha


if __name__ == '__main__':
  for sha, seen_sha in load_map():
    print sha, '->', seen_sha


##if __name__ == '__main__':
##  wc = WorldCache()
##  sha = wc.commit_list()[2]
##  I = wc.get_pickle_from_sha(sha)
##  ooo = wc.commit_new(I)
