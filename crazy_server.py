from traceback import format_exc
from wsgiref.simple_server import make_server
import sys
sys.path.insert(0, './dulwich-0.9.0.zip/dulwich-0.9.0')
from dulwich.repo import Repo, NotGitRepository
from gitty import WorldCache
from html import render, commit_list


cache = WorldCache()


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
    return ok200(start_response, commit_list(cache.commit_list()))

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

