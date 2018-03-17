from __future__ import absolute_import

import sys
from pdb import Pdb as _Pdb

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

