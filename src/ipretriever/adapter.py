#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import urllib.request
import re
import ipretriever
import random
import logging

class Generic(object):

  TIMEOUT = 30

  def __init__(self, url_page):
    self.url_page = url_page

  def get_public_ip(self):
    """Returns the current public IP address. Raises an exception if an issue occurs."""
    try:
      f = urllib.request.urlopen(self.url_page, timeout=self.TIMEOUT)
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

ALL = [
  IfConfig,
  IPEcho,
  TrackIP,
]

def get_ip(try_count):
  logger = logging.getLogger("get_ip")
  errors = []
  for i in range(try_count):
    try:
      logger.debug("Loop %d/%d", i + 1, try_count)
      provider = random.choice(ALL)()
      logger.debug("Provider : %s" % provider.url_page)
      ip = provider.get_public_ip()
      logger.debug("Gor ip %s" % provider.url_page)
      return ip
    except ipretriever.Fault as e:
      er = repr(e)
      logger.error("Fail to get ip : %s", er)
      errors.append(er)
  raise ipretriever.Fault("Fail to get ip after %d tries (%s)" % (try_count, ",".join(errors)))
