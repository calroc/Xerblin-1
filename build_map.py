from operator import attrgetter
import sys
sys.path.insert(0, './dulwich-0.9.0.zip/dulwich-0.9.0')
from dulwich.repo import Repo
from gitty import load_latest_state, pickle_name


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
