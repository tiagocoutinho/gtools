# -*- coding: utf-8 -*-
#
# This file is part of the gtools project
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT License. See LICENSE for more info.

from __future__ import absolute_import

__all__ = 'Greenlet',

import weakref

import gevent

_Greenlet = gevent.Greenlet


class Greenlet(_Greenlet):

    def __init__(self, *args, **kwargs):
        super(Greenlet, self).__init__(*args, **kwargs)
        self._caller_ = gevent.getcurrent()
