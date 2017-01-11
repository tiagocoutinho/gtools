from __future__ import absolute_import

import gevent.greenlet

from .greenlet import Greenlet

def patch_all(gevent=True):
    if gevent:
        patch_gevent()


def patch_gevent(greenlet=True):
    if greenlet and gevent.Greenlet != Greenlet:
        gevent.Greenlet = Greenlet
        gevent.greenlet.Greenlet = Greenlet
        gevent.spawn = Greenlet.spawn
        gevent.spawn_later = Greenlet.spawn_later