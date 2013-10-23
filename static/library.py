def dup(I):
    '''
    "Duplicate" the top item on the stack.
    '''
    stack, dictionary = I
    return (stack[0], stack), dictionary


