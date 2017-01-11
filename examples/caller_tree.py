import gevent

from gtools.monkey import patch_all
patch_all()

from gtools.tree import CallerTree


def ptree(message, greenlets=None):
    print(80*'=')
    print(message)
    print(CallerTree(greenlets=greenlets))
    print(80*'-')


def go(level):
    if level > 0:
        gevent.spawn(go, level-1).join()
    else:
        gevent.sleep(1)
        print('go() at level 0')

ptree('Gevent caller tree before start:')

top_greenlet = gevent.spawn(go, 5)
# just to trigger all the greenlet chain
gevent.sleep(1E-3)

ptree('Gevent caller during execution:')

top_greenlet.join()

ptree('Gevent caller tree after finish:')
