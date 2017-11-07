#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import getopt
import urllib.request
import json
import logging
import ipretriever
import ipretriever.adapter

API_KEY = ''
DOMAIN_NAME = 'mydomain.com'
TTL = 300

RECORD = {'type': 'A', 'name': '@'}

LOG_LEVEL = logging.INFO
LOG_FILE = 'gandyn.log'

IP_TRY_COUNT = 5

class GandiDomainUpdater(object):
  """Updates a gandi DNS record value."""
  def __init__(self, api_key, domain_name, record):
    """Constructor

    Keyword arguments:
    api_key -- The gandi XML-RPC api key. You have to activate it on gandi website.
    domain_name -- The domain whose record will be updated
    record -- Filters that match the record to update
    """
    self.api_key = api_key
    self.domain_name = domain_name
    self.record = record
    self.__zone_id = None

  def __request(self, page, method, data):
    if (data):
      data = json.dumps(data).encode("utf8")
    req = urllib.request.Request('https://dns.api.gandi.net/api/v5/%s' % page, data=data, method=method)
    req.add_header('Content-type', 'application/json')
    req.add_header('X-Api-Key', self.api_key)
    res = urllib.request.urlopen(req)
    data = json.loads(res.read().decode('utf8'))
    return data
  
  def __get_active_zone_id(self):
    """Retrieve the domain active zone id."""
    if self.__zone_id is None:
      res = self.__request("zones", "GET", None)
      for z in res:
        if self.domain_name == z['name']:
            self.__zone_id = z['uuid']
            break      
    return self.__zone_id

  def __get_record_page(self):
    return "zones/%s/records/%s/%s" % (self.__get_active_zone_id(), self.record['name'], self.record['type'])

  def get_record_value(self):
    """Retrieve current value for the record to update."""
    try:
      res = self.__request(self.__get_record_page(), "GET", None)
      return res['rrset_values'][0]
    except urllib.error.HTTPError as e:
      if e.code == 404:
        return None
      raise

  def update_record_value(self, new_value, ttl=300):
    """Updates record value.

    Update is done on a new zone version. If an error occurs,
    that new zone is deleted. Else, it is activated.
    This is an attempt of rollback mechanism.
    """
    data = {
      "rrset_ttl" : ttl,
      "rrset_values" : [
        new_value
      ]
    }
    self.__request(self.__get_record_page(), "PUT", data)


def usage(argv):
  print(argv[0], ' [[-c | --config] <config file>] [-h | --help]')
  print('\t-c --config <config file> : Path to the config file')
  print('\t-h --help                 : Displays this text')


def main(argv, global_vars, local_vars):
  try:
    options, remainder = getopt.getopt(argv[1:], 'c:h', ['config=', 'help'])
    for opt, arg in options:
      if opt in ('-c', '--config'):
        config_file = arg
        # load config file
        exec(
            compile(open(config_file).read(), config_file, 'exec'),
            global_vars,
            local_vars
        )
      elif opt in ('-h', '--help'):
        usage(argv)
        exit(1)
  except getopt.GetoptError as e:
    print(e)
    usage(argv)
    exit(1)

  try:
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        level=LOG_LEVEL,
        filename=LOG_FILE)
    gandi_updater = GandiDomainUpdater(API_KEY, DOMAIN_NAME, RECORD)
    # get DNS record ip address
    previous_ip_address = gandi_updater.get_record_value()
    logging.debug('DNS record IP address : %s', previous_ip_address)

    # get current ip address
    current_ip_address = ipretriever.adapter.get_ip(IP_TRY_COUNT)
    logging.debug('Current public IP address : %s', current_ip_address)

    if current_ip_address != previous_ip_address:
      # update record value
      gandi_updater.update_record_value(current_ip_address, TTL)
      logging.info('DNS updated')
    else:
      logging.debug('Public IP address unchanged. Nothing to do.')
  except urllib.error.HTTPError as e:
    logging.error('An error occured using Gandi API : %s ', e)
  except ipretriever.Fault as e:
    logging.error('An error occured retrieving public IP address : %s', e)

main(sys.argv, globals(), locals())
