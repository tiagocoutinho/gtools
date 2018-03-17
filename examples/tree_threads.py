# -*- coding: utf-8 -*-
#
# This file is part of the gtools project
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT License. See LICENSE for more info.

"""\
This example demonstrates how to display greenlet information in a tree
from greenlets started in different threads
"""

from gtools.monkey import patch_all
patch_all()

import threading
import gevent

from gtools.tree import Tree


def ptree(message, tree=None):
    print(80*'-')
    print(message)
    if tree is None:
        tree = Tree()
    print(tree)
    return tree


def inner_loop(name):
    gevent.sleep(1)


def outer_loop(name):
    gevent.spawn(inner_loop, name).join()


def spawn_thread(target, i):
    thread = threading.Thread(target=target, name='T%d' % i,
                              args=('thread %d' % i,))
    thread.start()
    return thread


def joinall_thread(threads):
    map(threading.Thread.join, threads)


def main():
    print(__doc__)

    gs = [gevent.spawn(outer_loop, 'greenlet %d' % i) for i in range(3)]
    gevent.sleep()
    ptree('Gevent tree after greenlets loop start:')

    ts = [spawn_thread(outer_loop, i) for i in range(3)]

    tree1 = ptree('Gevent tree after thread loop start:')

    print('Waiting ~1s for all greenlets to finish')
    gevent.joinall(gs)
    joinall_thread(ts)
    ptree('Gevent tree after all greenlets finished:', tree1)

    del gs
    del ts

    ptree('Gevent tree after all greenlets finished and dereferenced:', tree1)

    ptree('New gevent tree:')


if __name__ == '__main__':
    main()
