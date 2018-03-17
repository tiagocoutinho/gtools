# gtools

A python library providing [gevent](http://www.gevent.org) tools:

* a gevent friendly pdb
* tree representation of running greenlets


## Gevent friendly pdb

The *standard* python `pdb` module blocks all greenlets at the pdb prompt
(unlike a threaded app). If you want your greenlets to run in the background
you can use `gtools.pdb` instead.

It can be used like the standard `pdb`.

So, imagine you have a gevent app that you want to debug:

```python
# ======
# app.py
# ======

import gevent

def produce(p):
    for i in range(60):
        p.append(i)
        gevent.sleep(1)

products = []
gevent.spawn(produce, products)
```

to debug it just type on the console:

```bash
$ python -m gtools.pdb app.py
```

Then hit '**n**' until you reach the `task.join()` line. At this point the
greenlet is already doing its work on the background. To make sure just type
*products* several times on the pdb console and you will see the products list
being filled by the running greenlet:

```bash
> /app.py(9)<module>()
-> gevent.spawn(produce, products)
(Pdb) products
[0, 1, 2]
(Pdb) products
[0, 1, 2, 3, 4, 5, 6, 7]
```

Use `gtools.pdb.set_trace()` just as you would with the standard
`pdb.set_trace()`

## Monitoring greenlets

`gtools.tree.Tree()` allows you to trace the current greenlets and display them
in a tree like structure:

```python

>>> import gevent
>>> import gtools.tree

>>> def iloop():
...     gevent.sleep(1)

>>> def oloop():
...     gtools.spawn(iloop)
...     gevent.sleep(0.5)

>>> task = gtools.spawn(oloop)

>>> # sleep just to trigger spawn of inner greenlets
>>> gevent.sleep()
>>> tree = gtools.tree.Tree()

>>> # initial status
>>> print(tree)
Root
└─ <greenlet.greenlet A> status=running
    └─ <Greenlet B: oloop> status=running
        └─ <Greenlet C: iloop> status=running

>>> # after outer loop finishes
>>> gevent.sleep(0.6)
>>> print(tree)
Root
└─ <greenlet.greenlet A> status=running
    └─ <Greenlet B: oloop> status=finished:success
        └─ <Greenlet C: iloop> status=running

>>> # after inner loop finishes
>>> gevent.sleep(0.6)
>>> print(tree)
Root
└─ <greenlet.greenlet A> status=running
    └─ <Greenlet B: oloop> status=finished:success
        └─ <Greenlet C: iloop> status=dead:garbage collected

>>> del task

>>> # when there are no more references to the greenlets
>>> print(tree)
Root
└─ <greenlet.greenlet A> status=running
    └─ <Greenlet B: oloop> status=dead:garbage collected
        └─ <Greenlet C: iloop> status=dead:garbage collected

>>>
>>> # new tree
>>> print(gtools.tree.Tree())
Root
```

The above example requires the usage of `gtools.Greenlet`.

To trace greenlets from an existing gevent application you simply need to
*monkey-patch* gevent itself **before** importing your app:

```python
# ======
# app.py
# ======

import gevent

def iloop():
    gevent.sleep(1)

def oloop():
    gevent.spawn(iloop)
    gevent.sleep(0.5)

def run():
    return gevent.spawn(oloop)
```

```python
>>> from gtools.monkey import patch_gevent
>>> patch_gevent()
>>> import app
>>> import gtools.tree

>>> the_app = app.run()

>>> # sleep just to trigger spawn of inner greenlets
>>> gevent.sleep()
>>> tree = gtools.tree.Tree()

>>> # initial status
>>> print(tree)
Root
└─ <greenlet.greenlet A> status=running
    └─ <Greenlet B: oloop> status=running
        └─ <Greenlet C: iloop> status=running
```

If you don't monkey patch, you can still have limited information about the
running greenlets (notice that the tree hierarchy is lost):

```python

>>> import app
>>> import gtools.tree
>>> task = gevent.spawn(oloop)

>>> the_app = app.run()

>>> # sleep just to trigger spawn of inner greenlets
>>> gevent.sleep()
>>> tree = gtools.tree.Tree(all=True)

>>> # initial status
>>> print(tree)
Root
└─ <greenlet.greenlet A> status=running
    └─ <Hub [...]> status=running
        ├─ <Greenlet B: oloop> status=running
        └─ <Greenlet C: iloop> status=running
```

It can even trace greenlets across multiple threads (see
`examples/tree_threads.py`)
