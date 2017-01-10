import gc
import gevent
import threading

from gtools.tree import Tree

N = 1

def ptree(message, greenlets=None):
    print(80*'-')
    print(message)
    print(Tree(greenlets=greenlets))

def loop(name, n):
    for i in range(n):
        gevent.sleep(1)

ptree('Gevent tree before start:')

gs = [gevent.spawn(loop, 'loop greenlet %d' %i, n=N)
      for i in range(10)]

ptree('Gevent tree after greenlets loop started:')

gevent.joinall(gs)

# make sure there are no references to the greenlets
del gs
gc.collect(2)

ptree('Gevent tree after greenlets loop finished:')

