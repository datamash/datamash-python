#!/usr/bin/env python
# encoding: utf-8
"""
datamash.py
Copyright (c) 2013 DatamashIO, All rights reserved.
"""

import re
import requests
import simplejson
import urllib
import urllib2


API_HOST = 'datamash.io'
API_PORT = 443
API_VERSION = 'kowalski'
API_VERIFY_SSL = True

VALID_SERIES_KEY = r'^[a-zA-Z0-9\.:;\-_/\\ ]*$'
RE_VALID_SERIES_KEY = re.compile(VALID_SERIES_KEY)



class Client(object):

    def __init__(self, key, host=API_HOST, port=API_PORT, secure=True, pool_connections=10, pool_maxsize=10):
      self.key = key
      self.host = host
      self.port = port
      self.secure = secure
      self.session = requests.session()
      self.session.mount('http://', requests.adapters.HTTPAdapter(pool_connections=pool_connections, pool_maxsize=pool_maxsize))
      self.session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=pool_connections, pool_maxsize=pool_maxsize))

    def repositories(self):
      json = self.request('/repositories', method='GET')
      return map(lambda j: Repository.from_json(j), json)

    def repository(self, name):
      json = self.request('/repositories/%s' % (name,), method='GET')
      json.update({"client": self})
      return Repository(**json)

    def create_repository(self, name, **params):
      params.update({
        "name": name
      })
      json = self.request('/repositories', method='POST', params=params)
      return Repository.from_json(json)

    def _get_repository_resources(self, repository_key):
      json = self.request('/repositories/%s/resources' % (repository_key,), method='GET')
      return map(lambda j: Resource(**dict(j.items() + {"client": self}.items())), json)

    def _synchronize_repository(self, repository):
      self.request('/repositories/%s/sync' % (repository.id,), method='POST', params={})

    def _get_repository_resource(self, repository, resource_key):
      json = self.request('/repositories/%s/resources/%s' % (repository.key, resource_key), method='GET')
      return Resource(**dict(json.items() + {"client": self}.items()))

    def _resource_data(self, resource):
      return self.request('/resources/%s/data' % (resource.id, ), method='GET')


    def _resource_natural_language_query(self, resource, query):
      return self.request('/resources/%s?query=%s' % (resource.id, query), method='GET')

    def request(self, target, method='GET', params={}):
        assert method in ['GET', 'POST', 'PUT', 'DELETE'], "Only 'GET', 'POST', 'PUT', 'DELETE' are allowed for method."

        headers = {
            'User-Agent': 'datamash-python/%s' % (API_VERSION, ),
            'Accept-Encoding': 'application/json', #'gzip',
        }

        if method == 'POST':
            headers['Content-Type'] = "application/json"
            base = self.build_full_url(target)
            print params
            response = self.session.post(base, data=simplejson.dumps(params), auth=(self.key, ''), headers=headers, verify=API_VERIFY_SSL)
        elif method == 'PUT':
            headers['Content-Type'] = "application/json"
            base = self.build_full_url(target)
            response = self.session.put(base, data=simplejson.dumps(params), auth=(self.key, ''), headers=headers, verify=API_VERIFY_SSL)
        elif method == 'DELETE':
            base = self.build_full_url(target, params)
            response = self.session.delete(base, auth=(self.key, ''), headers=headers, verify=API_VERIFY_SSL)
        else:
            base = self.build_full_url(target, params)
            response = self.session.get(base, auth=(self.key, ''), headers=headers, verify=API_VERIFY_SSL)

        if response.status_code == 200:
            if response.text:
                json = simplejson.loads(response.text)
            else:
                json = ''
            #try:
            #    json = simplejson.loads(response.text)
            #except simplejson.decoder.JSONDecodeError, err:
            #    json = dict(error="JSON Parse Error (%s):\n%s" % (err, response.text))
        else:
          raise DatamashAPIException(simplejson.loads(response.text)['error'])
        return json

    def build_full_url(self, target, params={}):
        default_port = {80: not self.secure, 443: self.secure}
        port = "" if default_port.get(self.port, False) else ":%d" % self.port
        protocol = "https://" if self.secure else "http://"
        base_full_url = "%s%s%s" % (protocol, self.host, port)
        return base_full_url + self.build_url(target, params)

    def build_url(self, url, params={}):
        if params:
            return "/%s%s?%s" % (API_VERSION, url, self._urlencode(params))
        else:
            return "/%s%s" % (API_VERSION, url)

    def _urlencode(self, params):
        p = []
        for key, value in params.iteritems():
            if isinstance(value, (list, tuple)):
                for v in value:
                    p.append((key, v))
            elif isinstance(value, dict):
                for k, v in value.items():
                    p.append(('%s[%s]' % (key, k), v))
            else:
                p.append((key, value))
        return urllib.urlencode(p).encode("UTF-8")





class Repository(object):

  def __init__(self, **kwargs):
    self.client = kwargs.get('client', None)
    self.id = kwargs.get('id','')
    self.key = kwargs.get('key','')
    self.name = kwargs.get('name','')
    self.status = kwargs.get('status','')

  def to_json(self):
    return {"id": self.id, "key": self.key, "name": self.name, "status": self.status}

  def synchronize(self):
    return self.client._synchronize_repository(self)

  def resources(self):
    return self.client._get_repository_resources(self.key)

  def resource(self, resource_key):
    return self.client._get_repository_resource(self, resource_key)




class Resource(object):

  def __init__(self, **kwargs):
    self.client = kwargs.get('client', None)
    self.id = kwargs.get('id','')
    self.key = kwargs.get('key','')
    self.schema = kwargs.get('schema',{})
    self.count = kwargs.get('count',0)

  def query(self, query):
    return self.client._resource_natural_language_query(self, query)

  def data(self):
    return self.client._resource_data(self)

  def to_json(self):
    return {
      "id": self.id,
      "key": self.key,
      "schema": self.schema,
      "count": self.count
    }


class DatamashAPIException(Exception):
    pass