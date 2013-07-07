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
from xerblin import items, get
from html import HTML


def key_get(dictionary, key, default=None):
  try:
    return get(dictionary, key)
  except KeyError:
    return default


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


def use_js(h):
  h.script(src='/static/jquery-1.10.2.min.js', charset='utf-8')
  h.script(src='/static/d3.v3.min.js', charset='utf-8')


def render(interpreter):
  ht = HTML()
  d = interpreter[1]
  title = key_get(d, 'title', 'A Title')
  with ht.head as h:
    h.title(title)
    h.meta(charset='utf-8')
    h.link(rel='stylesheet', href='./static/site.css')
    extra_head = key_get(d, 'extra_head')
  with ht.body as b:
    b.h1(title)
    b.h3('A DeltaBot')
    b.div(id_='viewer', style='float:left').svg(width='1000px', height='128px')
    display_interpreter(b, interpreter)
    b.script('''
var data;
var svg;


$(function() {

data = [
    {x:23, y:18},
    {x:99, y:18},
    {x:23, y:28},
    {x:99, y:28},
    ];

svg = d3.select("svg");
svg.selectAll("circle")
    .data(data)
    .enter().append("svg:circle")
    .attr("cx", function(d) {return d.x})
    .attr("cy", function(d) {return d.y})
    .attr("r", "3px")
    ;

})
''')
  return ht


if __name__ == '__main__':
  from xerblin import ROOT, insert
  d = insert(ROOT[1], 'title', 'DeltaBot Demo Page')
  s = (23, ('34', ((abs, 2, '3'), (88, ()))))
  I = s, d
  print render(I)
