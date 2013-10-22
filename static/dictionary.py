
def insert(node, key, value):
    '''
    Return a tree with value stored under key. Replaces old value if any.
    '''
    if not node:
        return key, value, (), ()

    node_key, node_value, lower, higher = node

    if key < node_key:
        return node_key, node_value, insert(lower, key, value), higher

    if key > node_key:
        return node_key, node_value, lower, insert(higher, key, value)

    return key, value, lower, higher


def get(node, key):
    '''
    Return the value stored under key or raise KeyError if not found.
    '''
    if not node:
        raise KeyError(key)

    node_key, value, lower, higher = node

    if key == node_key:
        return value

    return get(lower if key < node_key else higher, key)


def delete(node, key):
    '''
    Return a tree with the value (and key) removed or raise KeyError if
    not found.
    '''
    if not node:
        raise KeyError(key)

    node_key, value, lower, higher = node

    if key < node_key:
        return node_key, value, delete(lower, key), higher

    if key > node_key:
        return node_key, value, lower, delete(higher, key)

    # So, key == node_key, delete this node itself.

    # If we only have one non-empty child node return it.  If both child
    # nodes are empty return an empty node (one of the children.)
    if not lower:
        return higher
    if not higher:
        return lower

    # If both child nodes are non-empty, we find the highest node in our
    # lower sub-tree, take its key and value to replace (delete) our own,
    # then get rid of it by recursively calling delete() on our lower
    # sub-node with our new key.
    # (We could also find the lowest node in our higher sub-tree and take
    # its key and value and delete it. I only implemented one of these
    # two symmetrical options. Over a lot of deletions this might make
    # the tree more unbalanced.  Oh well.)
    node = lower
    while node[3]:
        node = node[3]
    key, value = node[:2]

    return key, value, delete(lower, key), higher

