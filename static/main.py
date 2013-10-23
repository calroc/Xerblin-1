

STACK = ()
DICTIONARY = insert((), "dup", dup)


def interp():
  global STACK
  global DICTIONARY
  command = doc["zone"].value
  STACK, DICTIONARY = interpret((STACK, DICTIONARY), command)
  ist()


def pu():
  global STACK
  STACK = push(STACK, doc["zone"].value)
  ist()


def dr():
  global STACK
  it, STACK = pop(STACK, 1)
  doc["zone"].value = it
  ist()


def pik():
  global STACK
  n = int(doc["zone"].value)
  it, STACK = pick_(STACK, n)
  doc["zone"].value = it


def ist():
  doc["display"].innerHTML = str(list(iterStack(STACK)))

