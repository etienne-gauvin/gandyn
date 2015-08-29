#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import urllib.request
import re
import ipretriever

class Generic(object):
  def __init__(self, url_page):
    self.url_page = url_page

  def get_public_ip(self):
    """Returns the current public IP address. Raises an exception if an issue occurs."""
    try:
      f = urllib.request.urlopen(self.url_page)
      data = f.read().decode("utf8")
      f.close()
      pattern = re.compile('\d+\.\d+\.\d+\.\d+')
      result = pattern.search(data, 0)
      if result is None:
        raise ipretriever.Fault('Service ' + self.url_page + ' failed to return the current public IP address')
      else:
        return result.group(0)
    except urllib.error.URLError as e:
      raise ipretriever.Fault(e)

class IfConfig(Generic):
  def __init__(self):
    super(IfConfig, self).__init__('http://ifconfig.me/ip')

class IPEcho(Generic):
  def __init__(self):
    super(IPEcho, self).__init__('http://ipecho.net/plain')

class TrackIP(Generic):
  def __init__(self):
    super(TrackIP, self).__init__('http://www.trackip.net/ip')
