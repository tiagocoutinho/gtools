from __future__ import absolute_import

__all__ = 'Tree',

import treelib
import greenlet

from . import base


def Tree(greenlets=None):
    """
    Create a class:`treelib.Tree` with nodes corresponding to the greenlets.

    To handle the case where the python process has more than one thread with
    its own gevent loop, the root node of the tree is spurious in the sence that
    its sole purpose is to provide a single common parent to each thread event
    loop greenlet.

    Keyword Args:
        greenlets: a greenlet or a sequence of greenlets. None means find all
                   existing greenlet objects [default: None].
    Returns:
        treelib.Tree: a tree object
    """
    def add(tree, g):
        gid = base.greenlet_id(g)
        if tree.contains(gid):
            return
        tag = base.greenlet_tag(g)

        if g.parent is None:
            parent = '__root__'
        else:
            add(tree, g.parent)
            parent = base.greenlet_id(g.parent)
        tree.create_node(tag=tag, identifier=gid, parent=parent)

    if greenlets is None:
        greenlets = base.igreenlets()
    elif isinstance(greenlets, greenlet.greenlet):
        greenlets = greenlets,

    tree = treelib.Tree()
    tree.create_node('Root', '__root__')
    for g in greenlets:
        add(tree, g)

    return tree
