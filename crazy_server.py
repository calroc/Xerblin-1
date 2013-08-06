from pickle import Unpickler
from StringIO import StringIO
from traceback import format_exc
from wsgiref.simple_server import make_server
import sys
sys.path.insert(0, './dulwich-0.9.0.zip/dulwich-0.9.0')
from dulwich.repo import Repo, NotGitRepository
from templates import render, commit_list
from xerblin import interpret


pickle_name = 'system.pickle'
cache = {}


def load_latest_state(data):
  load = Unpickler(StringIO(data)).load
  # Pull out all the sequentially saved state, command, state, ... data.
  # This loop will break after the last saved state is loaded leaving
  # the last saved state in the 'state' variable
  while True:
    try:
      state = load()
    except EOFError:
      break
  return state


def start(start_response, message, mime_type):
  start_response(message, [('Content-type', mime_type)])


def err500(start_response, message):
  start(start_response, '500 Internal Server Error', 'text/plain')
  return [str(message)]


def ok200(start_response, response):
  start(start_response, '200 OK', 'text/html')
  return response


def report_problems(f):
  def inner(environ, start_response):
    try:
      return f(environ, start_response)
    except:
      return err500(start_response, format_exc())
  return inner


@report_problems
def x(environ, start_response):
  path = environ['PATH_INFO'].lstrip('/').split('/', 1)

  if path == ['']: # Root
    return ok200(start_response, commit_list(cache.keys()))

  sha = path[0]
  if len(sha) != 40:
    raise ValueError('incorrect length %r' % (sha,))
  if not sha.isalnum():
    raise ValueError('invalid %r' % (sha,))

  I = cache.get(sha)
  if not I:
    raise ValueError('unknown %r' % (sha,))

  if len(path) == 1: # Just render the current state.
    return ok200(start_response, render(I))

  command = path[1]
  if not command.isalnum():
    raise ValueError('invalid %r' % (command,))

  I = interpret(I, [command])
  return ok200(start_response, render(I))

##  start_response('501 Not Implemented', [('Content-type', 'text/plain')])
##  return ["D'oh! 501 Not Implemented ", repr(environ['PATH_INFO'])]


def run(app=x, host='', port=8000):
  httpd = make_server(host, port, app)
  httpd.serve_forever()


if __name__ == '__main__':
  repo = Repo('.')
  H = repo.revision_history(repo.head())

  print len(H), 'commits'
  for c in H:
    T = repo[c.tree]
    if pickle_name in T:
      _, sha = T[pickle_name] # mode is unused
      cache[c.id] = load_latest_state(repo[sha].data)
  print len(cache), 'trees'


  print "Serving on port http://localhost:8000/ ..."
  run()

