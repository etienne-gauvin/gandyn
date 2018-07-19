Gandyn
======

Your server has a dynamic IP address and you use Gandi as domain name server?
Then Gandyn is for you!

This is an unsecure script based on [Comète's work](http://gerard.geekandfree.org/blog/2012/03/01/debarrassez-vous-de-dyndns-en-utilisant-lapi-de-gandi/).
It uses [Gandi LiveDNS API](http://doc.livedns.gandi.net/) to update your DNS record.
Server public IP address is retrieved from many sources.

Prequisites
-----------
First of all you have to enable API interface for your domain on Gandi web interface.
Gandi will then give you an API key. Copy paste it to your gandyn config file. 


Installation
------------

The python standard way works.

    $ wget -O gandyn.tar.gz https://github.com/Chralu/gandyn/tarball/<version>
    $ tar xvzf gandyn.tar.gz
    $ cd gandyn/src/
    # python setup.py install
    
    
If you encounter issues with the xmlrpc.client missing module, you may try to install with Python 3.3 (or any other version 3 of python you may have)

    $ python3 setup.py install
  
Execution
---------
Add execute permission to gandyn.py

    chmod +x /usr/local/bin/gandyn.py

Gandyn gets its configuration from a simple python file. Config file syntax is described later.
To run Gandyn, use the command :

    gandyn.py --config <path to the config file>

To get Gandyn run every 5 minutes, add the following line to your crontab.

    */5 * * * * /usr/local/bin/gandyn.py --config <path to the config file>

Configuration
-------------
### Configuration File
Configuration file is a simple python script that defines global constants.

This is unsecure, so it is important that nobody can change the config file content.

Here is a basic config file with default values:

    #API key generated by Gandi
    API_KEY = '' 
    
    #Name of the domain to update
    DOMAIN_NAME = 'mydomain.net'

    #Time to live of the updated record
    TTL = 300
    
    #Filters used to find the record to update.
    #By default, the updated record is "@   A   xxx.xxx.xxx.xxx"
    #Where 'xxx.xxx.xxx.xxx' is the updated value
    RECORD = {'type':'A', 'name':'@'}
    
    #Log level of the script. Values are :
    #   logging.DEBUG
    #   logging.INFO
    #   logging.WARNING
    #   logging.ERROR
    #   logging.CRITICAL
    LOG_LEVEL = logging.DEBUG

    #Sharing id of the organisation 
    #SHARING_ID = ''
    
    #Path of the log file
    LOG_FILE = 'gandyn.log'

### Obtaining Sharing id
Zones can only be associated domains that share the same organization or, "sharing space". Therefore, If you want to create a new zone and attach it to a domain that is in an organization (ie. not your personal account), you must create the zone with the same SHARING_ID of the domain.

Unfortunately, there is no API that returns the SHARING_ID.To find the SHARING_ID, you must use the v5 of gandi website and navigate to the dashboard of the organization that owns the domain. The sharing_id will be in the URL and will immediateliy follow /dashboard/.
