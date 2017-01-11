# -*- coding: utf-8 -*-
#
# This file is part of the gtools project
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT License. See LICENSE for more info.

import sys
import weakref
import functools

import gevent
import gevent.local


class Multiplexer(object):

    class Channel(object):
        def __init__(self, name, manager):
            self.__name = name
            self.__manager = weakref.ref(manager)

        def __getattr__(self, name):
            std = self.__manager()._get_std(self.__name)
            return getattr(std, name)

    def __init__(self, stdout=True, stderr=True):
        self.active = False
        self.stdout = self.Channel('stdout', self) if stdout else None
        self.stderr = self.Channel('stderr', self) if stderr else None
        self._stdout = None
        self._stderr = None

        self.greenlets = {}
        self.data = gevent.local.local()

    def turn_on(self):
        if sys.stdout != self.stdout and self.stdout:
            self._stdout = sys.stdout
            sys.stdout = self.stdout
        if sys.stderr != self.stderr and self.stderr:
            self._stderr = sys.stderr
            sys.stderr = self.stderr
        self.active = True

    def turn_off(self):
        if self._stdout:
            sys.stdout = self._stdout
        if self._stderr:
            sys.stderr = self._stderr
        self.active = False

    def _get_std(self, std, greenlet=None):
        if greenlet is None:
            try:
                return getattr(self.data, std)
            except AttributeError:
                std_obj = self.__find_std(std)
                setattr(self.data, std, std_obj)
                return std_obj
        else:
            return self.__find_std(std, greenlet)

    def __find_std(self, std, greenlet=None):
        if greenlet is None:
            greenlet = gevent.getcurrent()
        try:
            return self.greenlets[id(greenlet)][std]
        except KeyError:
            if greenlet.parent is None:
                return getattr(sys, '__{0}__'.format(std))
            return self.__find_std(std, greenlet.parent)

    def __on_greenlet_finished(self, greenlet):
        del self.greenlets[id(greenlet)]

    def spawn(self, *args, **kwargs):
        greenlet = gevent.Greenlet(*args, **kwargs)
        self.register(greenlet)
        greenlet.start()
        return greenlet

    def register(self, greenlet, stdout=None, stderr=None):
        greenlet_id = id(greenlet)
        stdout = stdout or (self._stdout if self.active else sys.stdout)
        stderr = stderr or (self._stderr if self.active else sys.stderr)
        greenlet.link(self.__on_greenlet_finished)
        self.greenlets[greenlet_id] = dict(stdout=stdout, stderr=stderr)
        return greenlet_id

    def __enter__(self):
        self.turn_on()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.turn_off()


def example():
    import six

    def f(start, stop, step=1, sleep=0.1):
        print "loop", start, stop, step, sleep
        for i in range(start, stop, step):
            print(i)
            gevent.sleep(sleep)

    tasks = []
    with Multiplexer() as m:
        for i in range(2):
            task = gevent.Greenlet(f, i, 10, 2)
            task.stdout = six.StringIO()
            m.register(task, stdout=task.stdout)
            tasks.append(task)
            task.start()
        gevent.joinall(tasks)

    for task in tasks:
        print(' --- Output from {0} ---------'.format(task))
        print(task.stdout.getvalue())


if __name__ == "__main__":
    example()
