#!/usr/bin/env python
# encoding: utf-8

import datetime
import mock
import requests
import simplejson
import unittest
from unittest import TestCase
import datamash
from datamash import Client, Repository




class MockResponse(object):

  def __init__(self, status_code, text):
    self.status_code = status_code
    self.text = text



class ClientTest(TestCase):

  def setUp(self):
    self.client = Client('key', 'example.com', 443, True)
    self.client.session = mock.Mock()
    self.headers = {
      'User-Agent': 'datamash-python/%s' % datamash.version(),
      'Accept-Encoding': 'application/json',
    }
    self.get_headers = self.headers
    self.delete_headers = self.headers
    self.put_headers = dict({
        'Content-Type': 'application/json',
    }, **self.headers)
    self.post_headers = self.put_headers

  def test_init(self):
    client = Client('key', 'example.com', 80, False)
    self.assertEqual(client.key, 'key')
    self.assertEqual(client.host, 'example.com')
    self.assertEqual(client.port, 80)
    self.assertEqual(client.secure, False)


  def test_defaults(self):
    client = Client('key')
    self.assertEqual(client.host, 'datamash.io')
    self.assertEqual(client.port, 443)
    self.assertEqual(client.secure, True)

  def test_port_defaults(self):
    """ 80 is the default port for HTTP, 443 is the default for HTTPS """
    client = Client('key', 'example.com', 80, False)
    self.assertEqual(client.build_full_url('/etc'), 'http://example.com/kowalski/etc')
    client = Client('key', 'example.com', 88, False)
    self.assertEqual(client.build_full_url('/etc'), 'http://example.com:88/kowalski/etc')
    client = Client('key', 'example.com', 443, False)
    self.assertEqual(client.build_full_url('/etc'), 'http://example.com:443/kowalski/etc')
    client = Client('key', 'example.com', 443, True)
    self.assertEqual(client.build_full_url('/etc'), 'https://example.com/kowalski/etc')
    client = Client('key', 'example.com', 88, True)
    self.assertEqual(client.build_full_url('/etc'), 'https://example.com:88/kowalski/etc')
    client = Client('key', 'example.com', 80, True)
    self.assertEqual(client.build_full_url('/etc'), 'https://example.com:80/kowalski/etc')


  def test_connect_to_repository(self):
    self.client.session.get.return_value = MockResponse(200, """{
      "id": "1234567890",
      "url": "http://remote.com",
      "name": "http_remote_com",
      "description": "http_remote_com",
      "type": "Text",
      "number_of_resources": 1,
      "status": "ok",
      "version": 0,
      "timestamp": "2013-04-25T21:28:31Z"
    }""")
    repository = self.client.connect('http://remote.com')
    self.client.session.get.assert_called_once_with(
      'https://example.com/kowalski/repositories?url=http://remote.com&sync=true',
      auth=('key', ''),
      headers=self.get_headers
    )
    expected = Repository('id', 'url', 'name', 'description', 'type', 'number_of_resources', 'status', 'version', 'timestamp')
