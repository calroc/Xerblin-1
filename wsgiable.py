from sys import stderr
from traceback import format_exc
from types import FunctionType
from json import dumps
from os.path import exists
from urlparse import parse_qs
from wsgiref.simple_server import make_server
from xerblin import World, items


W = World()


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
  result = {"result": (stack, dictionary)}
  return dumps(result, default=_p, indent=2)


def get_session(environ):
  '''
  Return the World object for the request's session.
  (This is currently a stub that just returns the module
  global World.)
  '''
  return W


def get_form_values(environ):
  size = int(environ.get('CONTENT_LENGTH', 0))
  data = environ['wsgi.input'].read(size)
  return parse_qs(data)


def step(command, environ):
  w = get_session(environ)
  w.step(command.split())
  return as_json(w)


def x(environ, start_response):
  path = environ['PATH_INFO'].lstrip('/').split('/', 1)

  if path == ['']: # Root
    start_response('200 OK', [('Content-type', 'text/html')])
    return open('templates/index.html')

  if path == ['step']:
    form_data = get_form_values(environ)
    command = form_data.get('command', [''])[0]

    try:
      result = step(command, environ)
    except:
      start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
      return [format_exc()]

    start_response('200 OK', [('Content-type', 'application/json')])
    return result
  

  if len(path) == 2 and path[0] == 'static':
    fn = environ['PATH_INFO'].lstrip('/')
    if exists(fn) and  fn.endswith('.js'):
      start_response('200 OK', [('Content-type', 'application/javascript')])
      return open(fn)
  
  print >> stderr, path
  start_response('501 Not Implemented', [('Content-type', 'text/plain')])
  return ["D'oh! 501 Not Implemented ", repr(environ['PATH_INFO'])]


if __name__ == '__main__':
  httpd = make_server('', 8000, x)
  print "Serving on port 8000..."
  httpd.serve_forever()
