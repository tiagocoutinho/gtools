# -*- coding: utf-8 -*-
#
# This file is part of the gtools project
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT License. See LICENSE for more info.

from setuptools import setup, find_packages

import os


def main():
    _this_dir = os.path.dirname(__file__)
    r = {}
    with open(os.path.join(_this_dir, 'gtools', 'version.py')) as f:
        exec(f.read(), r)

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
        version=r['__version__'],
        packages=find_packages(),
        install_requires=[
            'six>=1.10',
            'gevent>=1.0',
            'treelib>=1.0',
            'geventhttpclient>=1.4'],
        license=r['__license__'],
        classifiers=CLASSIFIERS,
        author=r['__author__'],
        author_email=r['__author_email__'],
        description=r['__description__'],
        long_description=open('README.md').read(),
        long_description_content_type="text/markdown",
        url=r['__url__'],
        download_url=r['__download_url__'],
        platforms=r['__platforms__'],
        keywords=r['__keywords__'],
        )

if __name__ == '__main__':
    main()
