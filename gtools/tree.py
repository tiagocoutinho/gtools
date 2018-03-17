# -*- coding: utf-8 -*-
#
# This file is part of the gtools project
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT License. See LICENSE for more info.

from __future__ import absolute_import

__all__ = 'Tree', 'CallerTree'

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
            tag += 'dead, disappeared'
        elif isinstance(g, gevent.Greenlet):
            if g.ready():
                tag += 'finished ' + ('successfully' if g.successful() else 'with error')
            else:
                tag += 'running' if g else 'not started yet'
        else:
            tag += 'dead' if g.dead else 'running'
        return tag


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
        tag = GreenletTreeTag(g)

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


def CallerTree(greenlets=None):
    """
    Create a class:`treelib.Tree` with nodes corresponding to the greenlets.

    This tree is different from the :func:`Tree` if the greenlets are
    :class:`gtools.greenlet.Greenlet` since these greenlets keep track of the
    greenlets they were called from.

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
        tag = GreenletTreeTag(g)

        caller = base.caller(g)

        if caller is None:
            parent = '__root__'
        else:
            add(tree, caller)
            parent = base.greenlet_id(caller)
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
