from __future__ import absolute_import

import sys
from pdb import Pdb as _Pdb

from gevent.fileobject import FileObjectThread as File


class Pdb(_Pdb):
    def __init__(self, **kwargs):
        stdin = kwargs.get('stdin') or sys.stdin
        stdout = kwargs.get('stdout') or sys.stdout
        kwargs['stdin'] = stdin if isinstance(stdin, File) else File(stdin)
        kwargs['stdout'] = stdout if isinstance(stdout, File) else File(stdout)
        _Pdb.__init__(self, **_patch_pdb_args(kwargs))


def patch_pdb():
    import pdb
    pdb.Pdb = Pdb

