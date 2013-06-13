#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Copyright © 2012 Simon Forman
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
Run the Flask server with a World that stores its history in a git repo.
'''
from os.path import expanduser, exists, join
from argparse import ArgumentParser
import pickle, logging, sys
from dulwich.repo import Repo, NotGitRepository
from xerblin import World, items
import wsgiable


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


SYSTEM_PICKLE = 'system.pickle'


class CommitWorldMixin(object):

  def __init__(self, *a, **b):
    self.commit_thing = b.pop('commit_thing')
    super(CommitWorldMixin, self).__init__(*a, **b)

  def setCurrentState(self, state):
    super(CommitWorldMixin, self).setCurrentState(state)
    self.commit_thing()


class CommitWorld(CommitWorldMixin, World, object):
    pass


def make_commit_thing(path, files):
  log = logging.getLogger('COMMIT')
  try:
    repo = Repo(path)
  except NotGitRepository:
    log.critical("%r isn't a repository!", path)
    raise ValueError("%r isn't a repository!" % (path,))

  # Note that we bind the args as defaults rather than via a closure so
  # you can override them later if you want.
  def commit(files=files, repo=repo, log=log):
    repo.stage(files)
    commit_sha = repo.do_commit('autosave')
    log.info('commit %s', commit_sha)

  return commit


def initialize_repo(path, state):
  log = logging.getLogger('INIT_REPO')
  if not exists(path):
    log.critical("%r doesn't exist!", path)
    raise ValueError("%r doesn't exist!" % (path,))

  try:
    Repo(path)
  except NotGitRepository:
    # Good! That's what we expect.
    repo = Repo.init(path)
    log.info('%r created.', repo)
  else:
    # No good! We are an initialize function, nothing else.
    log.critical('Repository already exists at %r', path)
    raise ValueError('Repository already exists at %r' % (path,))

  system_pickle_file_name = join(path, SYSTEM_PICKLE)
  pickle.dump(state, open(system_pickle_file_name, 'wb'))
  log.info('%s written.', system_pickle_file_name)

  repo.stage([SYSTEM_PICKLE])
  staged = list(repo.open_index())
  log.info('Files staged: ' + ', '.join(['%s'] * len(staged)), *staged)
  commit = repo.do_commit('Initial commit.')
  log.info('Initial commit done. %s', commit)


# First parse command line args if any.
parser = ArgumentParser()
parser.add_argument(
  '-r', '--roost',
  default=expanduser('~/.pigeon'),
  help=('Use this directory as home for the Pigeon system. (default: %(default)s).\n'
        '(I apologize for the terrible pun.)'),
  )
parser.add_argument(
  '-i', '--init',
  default=False,
  action='store_true',
  help='Initialize the "roost" directory with git repo and system.pickle.',
  )
args = parser.parse_args()


if not exists(args.roost):
  print "Roost directory %r doesn't exist!" % (args.roost,)
  sys.exit(2)


# Initialize the "roost" directory if requested.
if args.init:
  from xerblin import ROOT
  initialize_repo(args.roost, ROOT)


state_file_name = join(args.roost, SYSTEM_PICKLE)
try:
  with open(state_file_name) as f:
    up = pickle.Unpickler(f)
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
  print 'Did you initialize roost? (Use "--init" command.)'
  sys.exit(e.errno)


# Create a commit_thing to let us save our state to the git repo after
# changes.
try:
  commit_thing = make_commit_thing(args.roost, [SYSTEM_PICKLE])
except ValueError, e:
  print e
  print 'Did you initialize roost? (Use "--init" command.)'
  sys.exit(2)


# Now that the config_file has had a chance to do its thing, import the
# system and run.
w = CommitWorld(
  initial=state,
  save_file=state_file_name,
  commit_thing=commit_thing,
  )


wsgiable.W = w
print "Serving on port 8000..."
wsgiable.run()
