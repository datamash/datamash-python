#!/usr/bin/env python
# encoding: utf-8
"""
datamash/__init__.py
Copyright (c) 2013 DatamashIO Ltd. All rights reserved.
"""

try:
    VERSION = __import__('pkg_resources').get_distribution('datamash').version
except Exception, e:
    VERSION = 'unknown'

def get_version():
    return VERSION

__version__ = get_version()

from datamash.client import *
from datamash.repository import *
from datamash.resource import *