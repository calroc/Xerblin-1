

def pop_TOS(I):
    '''
    Pop the top item off the stack and return it with the
    modified interpreter
    '''
    # This is a helper function factored out from handle_branch() and
    # handle_loop() below.
    (TOS, stack), dictionary = I
    return TOS, (stack, dictionary)


# These three following functions process the three kinds of combo-words.

def handle_sequence(I, seq):
    '''
    Run a sequence and return the modified interpreter.
    '''
    for func in seq[1:]:
        I = apply_func(I, func)
    return I


def handle_branch(I, branch):
    '''
    Check TOS and do one thing or another depending.
    '''
    TOS, I = pop_TOS(I)
    func = branch[(not TOS) + 1] # i.e. True = 1; False = 2
    return apply_func(I, func)


def handle_loop(I, loop):
    '''
    Check TOS and do body if it's true, repeat.
    '''
    while True:
        TOS, I = pop_TOS(I)
        if not TOS:
            break
        I = handle_sequence(I, loop)
    return I


# This primitive permits us to create a sort of "constant" in the dictionary.

def enstacken(I, stack_us):
    '''
    Push the items in the body onto the stack.
    '''
    stack, dictionary = I
    stack = push(stack, *stack_us[1:])
    return stack, dictionary


def apply_func(I, func):
    '''
    Given an interpreter and a function or combo-word tuple, apply the
    function or combo to the interpreter and return the modified
    interpreter.
    '''
    if isinstance(func, tuple):
        handler = func[0]
        I = handler(I, func)
    else:
        I = func(I)
    return I


# This is the main point of this module.  It implements the system with
# the help of the apply_func() function.
def interpret(I, command):
    '''
    Given an interpreter and a string command, interpret that string on
    the interpreter and return the modified interpreter.
    '''
    for word in command:

        # Is it an integer?
        try:
            literal = int(word)
        except ValueError:

            # Is it a float?
            try:
                literal = float(word)
            except ValueError:

                # Is it a string literal?
                if word.startswith('"') and word.endswith('"'):
                    literal = word[1:-1]

                # Nope, it must be a command word.
                else:
                    # Interpret the word.
                    func = get(I[1], word)
                    I = apply_func(I, func)
                    continue

        # A literal was found, push it onto the stack.
        I = (literal, I[0]), I[1]

    return I

