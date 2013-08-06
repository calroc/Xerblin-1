import logging
from os.path import join
from time import time
from operator import attrgetter
from pickle import Unpickler, dump
from StringIO import StringIO
import sys
sys.path.insert(0, './dulwich-0.9.0.zip/dulwich-0.9.0')
from dulwich.repo import Repo, NotGitRepository


sort_key = attrgetter('commit_time')
pickle_name = 'system.pickle'


path = '.'
repo = Repo(path)


def process_commits(repo):

  H = repo.revision_history(repo.head())
  H.sort(key=sort_key)

  for commit in H:

    tree = repo[commit.tree]

    try:
      blob_mode, blob_sha = tree[pickle_name]
    except KeyError:
#      print >> sys.stderr, commit.id, 'has no', pickle_name
      continue
#    print commit.id, pickle_name, blob_sha

    blob = repo[blob_sha]
    yield commit.id, load_latest_state(blob.data)


def load_latest_state(data):
  load = Unpickler(StringIO(data)).load
  state = None
  while True:
    try:
      state = load()
    except EOFError:
      break
  return state


I2SHA = {}
for sha, I in process_commits(repo):
  try:
    seen_sha = I2SHA[I]
  except KeyError:
    I2SHA[I] = sha
  else:
    print sha, '->', seen_sha
