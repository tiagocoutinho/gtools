import gc
import gevent
import threading

from gtools.tree import Tree

N1 = 2
N2 = 4

def ptree(message, greenlets=None):
    print(80*'-')
    print(message)
    print(Tree(greenlets=greenlets))

def loop(name, n):
    for i in range(n):
        gevent.sleep(1)

ptree('Gevent tree before start:')

gs = [gevent.spawn(loop, 'loop greenlet %d' %i, n=N1)
      for i in range(10)]

ptree('Gevent tree after greenlets loop start:')

def go(name, n):
    gevent.spawn(loop, name, n).join()
    h = gevent.get_hub()
    h.destroy(True)

[threading.Thread(target=go, args=('loop thread %d' % i, N2)).start()
 for i in range(2)]

ptree('Gevent tree after thread loop start:')

print('Waiting ~2s for all greenlets loop to finish')
gevent.joinall(gs)
del gs
ptree('Gevent tree after all greenlets loop finished:')

print('Waiting ~2s for thread loop to finish')
gevent.sleep(2)
ptree('Gevent tree after thread loop finished:')

gc.collect(2)
ptree('Gevent tree after thread loop finished and gc:')
