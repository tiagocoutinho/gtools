from __future__ import absolute_import

import sys
from pdb import Pdb as _Pdb
from pdb import main as _main

from gevent.fileobject import FileObjectThread as File


class Pdb(_Pdb):
    """Pdb object (gevent friendly).

    The interactive pdb console readline facilities are not supported
    (see `misinterpreting control keys`_).

    .. _`misinterpreting control keys`: https://github.com/gevent/gevent/issues/274
    """

    def __init__(self, **kwargs):
        stdin = kwargs.get('stdin') or sys.stdin
        stdout = kwargs.get('stdout') or sys.stdout
        kwargs['stdin'] = stdin if isinstance(stdin, File) else File(stdin)
        kwargs['stdout'] = stdout if isinstance(stdout, File) else File(stdout)
        _Pdb.__init__(self, **kwargs)

# Simplified interface

def run(statement, globals=None, locals=None):
    Pdb().run(statement, globals, locals)

def runeval(expression, globals=None, locals=None):
    return Pdb().runeval(expression, globals, locals)

def runcall(*args, **kwds):
    return Pdb().runcall(*args, **kwds)

def set_trace():
    frame = sys._getframe().f_back if hasattr(sys, '_getframe') else None
    Pdb().set_trace(frame)

def post_mortem(t=None):
    # handling the default
    if t is None:
        # sys.exc_info() returns (type, value, traceback) if an exception is
        # being handled, otherwise it returns None
        t = sys.exc_info()[2]
        if t is None:
            raise ValueError("A valid traceback must be passed if no "
                                               "exception is being handled")

    p = Pdb()
    p.reset()
    p.interaction(None, t)

def pm():
    post_mortem(sys.last_traceback)


def main():
    import pdb
    pdb.Pdb = Pdb
    pdb.main()


if __name__ == '__main__':
    main()
