#!/usr/bin/env python
# encoding: utf-8
"""
datamash.py
Copyright (c) 2013 DatamashIO Ltd. All rights reserved.
"""

import simplejson
from dateutil import parser


class Repository(object):

  def __init__(self, i, url, name, description, t, number_of_resources, status, version, timestamp):
    self.id = i
    self.url = url
    self.name = name
    self.description = description
    self.type = t
    self.number_of_resources = number_of_resources
    self.status = status
    self.version = version
    self.timestamp = timestamp
    self.client = None

  def set_client(self, client):
    self.client = client
    return self

  def to_json(self):
    return {
      "id": self.id,
      "url": self.url,
      "name": self.name,
      "description": self.description,
      "type": self.type,
      "number_of_resources": self.number_of_resources,
      "status": self.status,
      "version": self.version,
      "timestamp": self.timestamp
    }

  @property
  def resources(self):
    return self.client._repository_resources(self)

  @property
  def history(self):
    return self.client._repository_history(self)

  def get_version(self, version):
    return self.client._repository_version(self, version)

  def resource(self, name):
    return self.client._repository_resource(self, name).set_repository(self)

  @staticmethod
  def from_json(json):
    i = json.get('id', '')
    url = json.get('url', '')
    name = json.get('name', '')
    description = json.get('description', '')
    t = json.get('type', '')
    number_of_resources = json.get('number_of_resources', 0)
    status = json.get('status', '')
    version = json.get('version', '')
    timestamp = json.get('timestamp', '')
    repository = Repository(i, url, name, description, t, number_of_resources, status, version, timestamp)
    return repository
