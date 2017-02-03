#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup
from os.path import join, dirname

import re

with open(join(dirname(__file__), 'README.md'), encoding='utf-8') as fp:
    long_description = fp.read()


setup(
    name='pyxr',
    version='1.0.2',

    description="An object-relational mapping-ish wrapper around Xlib and X's resource manager/xrdb",
    long_description = long_description,

    url='https://github.com/WhatNodyn/Pyxr',
    author='Neil Cecchini',
    author_email='stranger.neil@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3 :: Only'
    ],

    packages=['pyxr'],
    install_requires=['python-xlib']
    
)
