# -*- coding: utf-8 -*-
#
# This file is part of the gtools project
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT License. See LICENSE for more info.

from __future__ import absolute_import

__all__ = ('caller', 'icallees',  'callees', 'is_running',
           'igreenlets', 'greenlets')

import gc

import gevent
import greenlet


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
    return g._caller_ if hasattr(g, '_caller_') else g.parent


def icallees(g):
    for gl in igreenlets():
        if caller(gl) == g:
            yield gl


def callees(g):
    return list(icallees(g))


def is_running(g):
    if isinstance(g, gevent.Greenlet):
        if not g:
            return False
        return not g.ready()
    else:
        return not g.dead


def igreenlets(filter=None):
    for g in gc.get_objects():
        if isinstance(g, greenlet.greenlet):
            if filter is None or filter(g):
                yield g


def greenlets(filter=None):
    return list(igreenlets(filter=filter))

