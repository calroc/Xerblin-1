from os.path import exists
from wsgiref.simple_server import make_server


h = lambda path: path.lstrip('/').split('/', 1)


def x(environ, start_response):
  path = h(environ['PATH_INFO'])

  if path == ['']:
    # Root
    start_response('200 OK', [('Content-type', 'text/html')])
    return open('templates/index.html')

  if len(path) == 2 and path[0] == 'static':
    fn = environ['PATH_INFO'].lstrip('/')
    if exists(fn) and  fn.endswith('.js'):
      start_response('200 OK', [('Content-type', 'application/javascript')])
      return open(fn)
  
  print path
  start_response('501 Not Implemented', [('Content-type', 'text/plain')])
  return ["D'oh! 501 Not Implemented ", repr(environ['PATH_INFO'])]


httpd = make_server('', 8000, x)
print "Serving on port 8000..."

# Serve until process is killed
httpd.serve_forever()
