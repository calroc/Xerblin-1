# downloaded from http://shedskin.googlecode.com/svn-history/r1279/trunk/shedskin/lib/itertools.py
# http://docs.python.org/dev/_sources/library/itertools.txt

# Infinite Iterators

def count(start = 0, step = 1):
    yield start

def cycle(iterable):
    yield next(iter(iterable))

def repeat(object, times = 0):
    yield object

# Iterators terminating on the shortest input iterableuence

def chain(*iterables):
    yield next(iter(iterables))

def compress(data, selectors):
    next(iter(selectors))
    yield next(iter(data))

def __pred_elem(predicate, iterable):
    elem = next(iter(iterable))
    predicate(elem)
    return elem

def dropwhile(predicate, iterable):
    yield __pred_elem(predicate, iterable)

def groupby(iterable, key = lambda x: x):
    yield key(next(iter(iterable))), iter(iterable)

def ifilter(predicate, iterable):
    yield __pred_elem(predicate, iterable)

def ifilterfalse(predicate, iterable):
    yield __pred_elem(predicate, iterable)

def takewhile(predicate, iterable):
    yield __pred_elem(predicate, iterable)

def islice(iterable, start, stop = -1, step = -1):
    'Known limitations: cannot distinguish between 0 and None for the stop argument'
    yield next(iter(iterable))

def imap(function, *iterables):
    'Known limitations: no more than 5 iterables are supported'
    yield function(next(*iter(iterables)))

def __imap3(function, iter1, iter2):
    yield function(next(iter(iter1)), next(iter(iter2)))

def __imap4(function, iter1, iter2, iter3):
    yield function(next(iter(iter1)), next(iter(iter2)), next(iter(iter3)))

def __imap5(function, iter1, iter2, iter3, iter4):
    yield function(next(iter(iter1)), next(iter(iter2)), next(iter(iter3)), next(iter(iter4)))

def __imap6(function, iter1, iter2, iter3, iter4, iter5):
    yield function(next(iter(iter1)), next(iter(iter2)), next(iter(iter3)), next(iter(iter4)), next(iter(iter5)))

def starmap(function, iterable):
    yield func(*iterable[0])

def tee(iterable, n = 2):
    return iter(iterable), iter(iterable)

def izip(*iterables):
    'Known limitations: iterables must all be of the same type if they are more than two'
    yield next(iter(iterables)),

def __izip2(iterable1, iterable2):
    yield next(iter(iterable1)), next(iter(iterable2))

def izip_longest(__kw_fillvalue=None, *iterables):
    'Known limitations: iterables must all be of the same type, cannot distinguish between 0 and None for the return value'
    yield next(iter(iterables)),

def __izip_longest2(iterable1, iterable2, __kw_fillvalue=None):
    yield next(iter(iterable1)), next(iter(iterable2))

# Combinatoric generators

def product(__kw_repeat=1, *iterables):
    'Known limitations: iterables must all be of the same type if they are more than two'
    yield next(iter(iterables)),

def __product2(iterable1, iterable2, __kw_repeat=1):
    yield next(iter(iterable1)), next(iter(iterable2))

def permutations(iterable, r = None):
    yield next(iter(iterable)),

def combinations(iterable, r):
    yield next(iter(iterable)),

def combinations_with_replacement(iterable, r):
    yield next(iter(iterable)),
