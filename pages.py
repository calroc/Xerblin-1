lib_scripts = [
  'http://cdnjs.cloudflare.com/ajax/libs/d3/3.0.1/d3.v3.min.js',
  'http://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.4.3/underscore-min.js',
  'http://cdnjs.cloudflare.com/ajax/libs/jquery/1.8.3/jquery.min.js',
  'http://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.9.2/jquery-ui.min.js',
  ]


lib_stylesheets = [
    'http://code.jquery.com/ui/1.9.2/themes/base/jquery-ui.css',
    ]

page = dict(
  title = "Hey There",
)


def my_ul(c, contents):
  '''
  Wrap the name, text pairs in contents in a UL element.
  The name is put in a SPAN element with the class "heavy" and the text
  gets " - " prepended to it.
  '''
  with c.ul as ul:
    for name, text in contents:
      li = ul.li
      li.span(name.title(), class_='heavy')
      li += ' - ' + text
    return ul


def body(b, title, things, **body_args):
  b.h1(title)
  b.h3('a Human-Computer Interface')
  b.p('Welcome to the Xerblin Demo, a live interactive interpreter embedded in a webpage.')
  with b.div(id_='docs') as docs:

    p = docs.p("Xerblin provides a single metaphor for interacting with"
               " computers that's simple enough to teach to children yet"
               " provides facilities that are useful to advanced programmers."
               " It can integrate all levels of software from the ")
    p.a('Desktop', href='http://thinkpigeon.blogspot.com/2012/12/crushingly-simple-user-interface.html')
    p += ' to '
    p.a('assembly language', href='https://github.com/PhoenixBureau/PigeonComputer/blob/master/docs/pigeon_firmware.rst')
    p += '.'

    docs.p('There are three basic user-facing elements to a Xerblin system.')

    my_ul(docs, things)


xerblin = dict(
  title = 'Xerblin Demo Page',
  scripts = lib_scripts + ['./static/xerblin.js'],
  stylesheets = lib_stylesheets,
  body = body,
  things = (
    ('Stack', 'a place to put objects for user manipulation. This is similar to a Clipboard but it can hold more than one item at a time. Commands operate on the items on the Stack.'),
    ('Dictionary', 'a place to keep commands. Any command that is inscribed in the Dictionary can be run from the user interface.'),
    ('Interpreter', 'A very simple command interpreter that takes care of running commands with the Stack.'),
    )
  )
