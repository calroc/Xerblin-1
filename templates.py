#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Copyright © 2013 Simon Forman
#
#    This file is part of Xerblin.
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
from xerblin import items
from html import HTML


def D(c, dictionary):
  for name, value in items(dictionary):
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
    t = c.li.ul
    for i in item:
      stack_item(t, i)
  else:
    c.li(str(item))


def display_interpreter(c, (stack, dictionary)):
  with c.div(id_='stack') as s:
    s.h3('Stack of Data')
    S(s.ul, stack)
  with c.div(id_='dictionary') as d:
    d.h3('Dictionary of Commands')
    D(d.div, dictionary)
  c.div(style='clear:both')
  with c.div(id_='interpreter') as d:
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
  from xerblin import ROOT
  s = (23, ('34', ((abs, 2, '3'), (88, ()))))
  I = s, ROOT[1]
  print render(I)
