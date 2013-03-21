from html import HTML


I = lambda foo, *a, **b: foo


def base(title, extra_head=I, scripts=(), stylesheets=(), body=I, html=None, **body_args):
  if html is None:
    html = HTML('html')

  with html.head as head:
    head.title(title)
    head.meta(charset='utf-8')
    extra_head(head)
    for script in scripts:
      head.script('', src=script)
    for stylesheet in stylesheets:
      head.link(rel='stylesheet', href=stylesheet)

  body(html.body, title, **body_args)

  return html


def my_ul(c, contents):
  with c.ul as ul:
    for name, text in contents:
      li = ul.li
      li.span(name.title(), class_='heavy')
      li += ' - ' + text
    return ul


def xerblin_body(body, title, subtitle, things, UL):
  body.h1(title)
  body.h3(subtitle)
  UL(body.div, things.iteritems())


if __name__ == '__main__':

  CDN = 'http://cdnjs.cloudflare.com/ajax/libs/'

  page = dict(

    scripts = [CDN + js_lib for js_lib in (
      'd3/3.0.1/d3.v3.min.js',
      'underscore.js/1.4.3/underscore-min.js',
      'jquery/1.8.3/jquery.min.js',
      'jqueryui/1.9.2/jquery-ui.min.js',
      )],

    stylesheets = ('http://code.jquery.com/ui/1.9.2/themes/base/jquery-ui.css',),

    body = xerblin_body,
    title = 'Xerblin',
    subtitle = 'a Human-Computer Interface',

    UL = my_ul,
    things = {
      'stack': 'a place to put objects for user manipulation. This is similar to a Clipboard but it can hold more than one item at a time. Commands operate on the items on the Stack.',
      'dictionary': 'a place to keep commands. Any command that is inscribed in the Dictionary can be run from the user interface.',
      'interpreter': 'a very simple command interpreter that takes care of running commands with the Stack. ',
      },

  )

  print '<!DOCTYPE html>'
  print base(**page)










































##def base(title, html=None):
##  if html is None:
##    html = HTML('html')
##  html.head.title(title)
##  with html.body as body:
##    with body.div(class_='header') as header:
##      header.h1(title)
##    with body.div(class_='content') as c:
##      c.p('Do I like it?')
##      c.p('Does it allow for {{ template_vars }} and such?')
##      c.p('What about in attributes?', class_='{{ question }}')
##  return html



