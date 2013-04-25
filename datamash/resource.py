#!/usr/bin/env python
# encoding: utf-8
"""
datamash.py
Copyright (c) 2013 DatamashIO Ltd. All rights reserved.
"""

import simplejson
from dateutil import parser



class Resource(object):

  def __init__(self, i, name, full_name, schema, number_of_records, version):
    self.id = i
    self.name = name
    self.full_name = full_name
    self.schema = schema
    self.number_of_records = number_of_records
    self.version = version
    self.client = None
    self.repository = None

  def set_client(self, client):
    self.client = client
    return self

  def set_repository(self, repository):
    self.repository = repository
    return self

  @property
  def data(self):
    return self.client._resource_data(self)

  #def query(self, query):
  #  return self.client._resource_natural_language_query(self, query)

  def to_json(self):
    return {
      "id": self.id,
      "name": self.name,
      "full_name": self.full_name,
      "schema": self.schema,
      "number_of_records": self.number_of_records
    }

  @staticmethod
  def from_json(json):
    i = json.get('id', '')
    name = json.get('name', '')
    full_name = json.get('full_name', '')
    schema = json.get('schema', '')
    number_of_records = json.get('number_of_records', 0)
    version = json.get('version', '')
    resource = Resource(i, name, full_name, schema, number_of_records, version)
    return resource




