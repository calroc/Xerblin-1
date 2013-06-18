from xerblin import items, ROOT
from html import HTML


def D(c, names):
  for name in names:
    with c.form(
      id_=name + '_form',
      action='/step',
      method='POST',
      class_='dictionary_word',
      ) as f:
      f.input(type_='text', name='command', value=name, style='display:none')
      f.input(type_='submit', value=name)


def S(c, stack):
  while stack:
    item, stack = stack
    stack_item(c, item)


def stack_item(c, item):
  if isinstance(item, basestring):
    c.li(repr(item))
  elif callable(item):
    c.li(item.__name__ + '()')
  elif isinstance(item, tuple):
    t = c.ul
    for i in item:
      stack_item(t, i)
  else:
    c.li(str(item))


def display_interpreter(c, (stack, dictionary)):
  with c.div(style='float:left') as s:
    s.h3('Stack of Data')
    S(s.ul, stack)
  with c.div(style='float:right;max-width:68%') as d:
    d.h3('Dictionary of Commands')
    D(d.div, (name for name, value in items(dictionary)))

  c.div(style='clear:both')

  with c.div as d:
    d.h3('Interpreter')
    with d.form(action='/step', method='POST') as f:
      f.input(name='command', type_='text')
      f.input(type_='submit', value='interpret')


def render(interpreter):
  ht = HTML()
  with ht.head as h:
    h.title('Xerblin Demo Page')
    h.meta(charset='utf-8')
    h.link(rel='stylesheet', href='./static/site.css')
  with ht.body as b:
    b.h1('Xerblin')
    display_interpreter(b, interpreter)
  return ht


if __name__ == '__main__':
  s = (23, ('34', ((abs, 2, '3'), (88, ()))))
  I = s, ROOT[1]
  print >> open('a.html', 'w'), render(I)
