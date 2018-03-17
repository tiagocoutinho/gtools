# -*- coding: utf-8 -*-
#
# This file is part of the gtools project
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT License. See LICENSE for more info.

from __future__ import absolute_import


def patch_all(gevent=True, pdb=True, **kwargs):
    if gevent:
        patch_gevent()
    if pdb:
        patch_pdb()
    from gevent.monkey import patch_all
    patch_all(**kwargs)


def patch_gevent(greenlet=True):
    import gevent.greenlet
    from .greenlet import Greenlet

    if greenlet and gevent.Greenlet != Greenlet:
        gevent.Greenlet = Greenlet
        gevent.greenlet.Greenlet = Greenlet
        gevent.spawn = Greenlet.spawn
        gevent.spawn_later = Greenlet.spawn_later


def patch_pdb():
    import pdb as _pdb
    from . import pdb
    _pdb.Pdb = pdb.Pdb
