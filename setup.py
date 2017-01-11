# -*- coding: utf-8 -*-
#
# This file is part of the gtools project
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT License. See LICENSE for more info.

from setuptools import setup, find_packages

import os
import sys


def main():
    sys.path.insert(0, os.path.dirname(__file__))
    import gtools

    CLASSIFIERS = """\
Intended Audience :: Developers
Intended Audience :: Science/Research
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Topic :: Software Development :: Libraries
Topic :: Utilities
""".splitlines()

    setup(
        name='gevent-tools',
        version=gtools.__version__,
        packages=find_packages(),
        install_requires=[
            'six>=1.10',
            'gevent>=1.0',
            'treelib>=1.0'],
        license=gtools.__license__,
        classifiers=CLASSIFIERS,
        author=gtools.__author__,
        author_email=gtools.__author_email__,
        description=gtools.__description__,
        long_description=open('README.md').read(),
        url=gtools.__url__,
        download_url=gtools.__download_url__,
        platforms=gtools.__platforms__,
        keywords=gtools.__keywords__,
        )

if __name__ == '__main__':
    main()
