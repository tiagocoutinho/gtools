# -*- coding: utf-8 -*-
#
# This file is part of the gtools project
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT License. See LICENSE for more info.

"""\
This example demonstrates how to display greenlet information in a tree without
monkey patching gevent itself.

You will notice that the inner loop greenlets are displayed at the same level
in the displayed tree as the outer loop since gtools has no information about
the greenlet tree.
"""

import gevent

from gtools import all_greenlets
from gtools.tree import Tree

def ptree(message, tree=None):
    print(80*'-')
    print(message)
    if tree is None:
        tree = Tree(greenlets=all_greenlets())
    print(tree)
    return tree


def inner_loop(name):
    gevent.sleep(1)

def outer_loop(name):
    task = gevent.spawn(inner_loop, name)
    gevent.sleep(1)
    task.join()

print(__doc__)

ptree('Gevent tree before start:')

gs = { gevent.spawn(outer_loop, 'loop greenlet %d' %i) for i in range(3) }
# the following is just to give time for the inner loop greenlets to spawn
gevent.sleep()

tree1 = ptree('Gevent tree after greenlets loop started:')

gevent.joinall(gs)

ptree('Gevent tree after greenlets finished:', tree=tree1)

# make sure there are no references to the greenlets
del gs

ptree('Gevent tree after greenlets finished and dereferenced:', tree=tree1)

ptree('New gevent tree:')

