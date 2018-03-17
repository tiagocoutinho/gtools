# -*- coding: utf-8 -*-
#
# This file is part of the gtools project
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT License. See LICENSE for more info.

from __future__ import absolute_import

__all__ = 'Tree',

import weakref

import treelib
import gevent
import greenlet

from . import base


class GreenletTreeTag(object):
    def __init__(self, greenlet):
        self._prefix = repr(greenlet) + ' status='
        self._greenlet = weakref.ref(greenlet)

    def __repr__(self):
        tag, g = self._prefix, self._greenlet()
        if g is None:
            tag += 'dead:garbage collected'
        elif isinstance(g, gevent.Greenlet):
            if g.ready():
                tag += 'finished:' + ('success' if g.successful() else 'error')
            else:
                tag += 'running' if g else 'not started yet'
        else:
            tag += 'dead' if g.dead else 'running'
        return tag

    def __lt__(self, other):
        return repr(self) < repr(other)


def Tree(greenlets=None, all=False):
    """
    Create a class:`treelib.Tree` with nodes corresponding to the greenlets.

    By default, this function only considers greenlets created with
    :class:`gtools.greenlet.Greenlet` or if the gevent module has been
    monkey patched with func:`gtools.monkey`.

    If you want to include non gtools greenlets call with
    `Tree(all=True)`.

    The tree starts with a spurious root node whoose goal is just to have
    a common node around greenlets started on different threads.

    Keyword Args:
        greenlets: a greenlet or a sequence of greenlets. None means find all
                   existing greenlet objects [default: None].
        all: when greenlets is None, if all is True, it will also search for
             non gtools greenlets
    Returns:
        treelib.Tree: a tree object
    """
    def add(tree, g):
        gid = base.greenlet_id(g)
        if tree.contains(gid):
            return
        tag = GreenletTreeTag(g)

        caller = base.caller(g)

        if caller is None:
            parent = '__root__'
        else:
            add(tree, caller)
            parent = base.greenlet_id(caller)
        tree.create_node(tag=tag, identifier=gid, parent=parent)

    if greenlets is None:
        if all:
            greenlets = base.all_greenlets_gen()
        else:
            greenlets = base.greenlets_gen()
    elif isinstance(greenlets, greenlet.greenlet):
        greenlets = greenlets,

    tree = treelib.Tree()
    tree.create_node('Root', '__root__')
    for g in greenlets:
        add(tree, g)

    return tree
