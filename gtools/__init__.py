# -*- coding: utf-8 -*-
#
# This file is part of the gtools project
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT License. See LICENSE for more info.

"""gevent utilities library"""

from . import version

__version__ = version.__version__
__description__ = version.__description__
__author__ = version.__author__
__author_email__ = version.__author_email__
__license__ = version.__license__
__url__ = version.__url__
__download_url__ = version.__download_url__
__platforms__ = version.__platforms__
__keywords__ = version.__keywords__
del version

from .base import *
