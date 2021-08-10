# -*- coding: utf-8 -*-
#
# This file is part of the gtools project
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT License. See LICENSE for more info.

from __future__ import absolute_import

__all__ = ('Greenlet', 'spawn', 'caller', 'callees_gen',  'callees',
           'is_running', 'greenlets_gen', 'greenlets',
           'all_greenlets_gen', 'all_greenlets')

import gevent
import greenlet

from .greenlet import _greenlets, Greenlet

spawn = Greenlet.spawn


def greenlet_id(g):
    return id(g)


def greenlet_tag(g):
    tag = repr(g)
    if isinstance(g, gevent.Greenlet):
        if g.ready():
            if g.successful():
                tag += ' status=finished (success)'
            else:
                tag += ' status=finished (error)'
        else:
            if g:
                tag += ' status=running'
            else:
                tag += ' status=not started yet'
    else:
        tag += ' dead={0}'.format(g.dead)
    return tag


def caller(g):
    return _greenlets.get(g, g.parent)


def callees_gen(g):
    for gl in greenlets_gen():
        if caller(gl) == g:
            yield gl


def callees(g):
    return list(callees_gen(g))


def is_running(g):
    if isinstance(g, gevent.Greenlet):
        if not g:
            return False
        return not g.ready()
    else:
        return not g.dead


def greenlets_gen(filter=None):
    for g in _greenlets:
        if filter is None or filter(g):
            yield g


def greenlets(filter=None):
    return list(greenlets_gen(filter=filter))


def all_greenlets_gen(filter=None):
    import gc
    for g in gc.get_objects():
        if isinstance(g, greenlet.greenlet):
            if filter is None or filter(g):
                yield g


def all_greenlets(filter=None):
    return list(all_greenlets_gen(filter=filter))
