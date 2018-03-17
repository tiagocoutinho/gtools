# -*- coding: utf-8 -*-
#
# This file is part of the gtools project
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT License. See LICENSE for more info.

"""\
This example demonstrates how to display greenlet information in a tree.

During the next minute 'products' will be feed from another greenlet just like a
real thread would.
"""

from gtools.monkey import patch_all
patch_all()

import pdb

import gevent


def produce(p):
    for i in range(60):
        p.append(i)
        gevent.sleep(1)


def main():

    products = []

    producer = gevent.spawn(produce, products)

    print(__doc__)
    print("Type 'products' several times to see it!")
    pdb.set_trace()


if __name__ == '__main__':
    main()
