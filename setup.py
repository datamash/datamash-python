#!/usr/bin/env python
# encoding: utf-8
"""
datamash-python/setup.py

Copyright (c) 2013 DatamashIO Ltd. All rights reserved.
"""

from setuptools import setup


install_requires = [
    'python-dateutil==1.5',
    'requests==1.0',
    'simplejson',
]


tests_require = [
    'mock',
    'unittest2',
]

setup(
    name="datamash",
    version="0.1.0",
    author="DatamashIO Ltd",
    author_email="dev@datamash.io",
    url="https://github.com/datamash",
    description="A client for the DatamashIO API",
    packages=["datamash"],
    long_description="A client for the DatamashIO API.",
    dependency_links=[
    ],
    setup_requires=['nose>=1.0'],
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite="tests"
)