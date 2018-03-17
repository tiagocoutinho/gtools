# -*- coding: utf-8 -*-
#
# This file is part of the gtools project
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT License. See LICENSE for more info.

"""\
This example demonstrates how to display greenlet information in a tree.
"""

from gtools.monkey import patch_all
patch_all()

import gevent

from gtools.tree import Tree


def ptree(message, tree=None):
    print(80*'-')
    print(message)
    if tree is None:
        tree = Tree()
    print(tree)
    return tree


def go(level):
    if level > 0:
        gevent.spawn(go, level-1).join()
    else:
        gevent.sleep(1)


def main():
    print(__doc__)

    ptree('Gevent tree before start:')

    top_task = gevent.spawn(go, 5)
    # the following is just to give time for the inner loop greenlets to spawn
    gevent.sleep(1e-6)

    tree1 = ptree('Gevent tree after greenlets loop started:')

    top_task.join()

    ptree('Gevent tree after greenlets finished:', tree=tree1)

    # make sure there are no references to the greenlets
    del top_task

    ptree('Gevent tree after greenlets finished and dereferenced:', tree=tree1)

    ptree('New gevent tree:')


if __name__ == '__main__':
    main()
