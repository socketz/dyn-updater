#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json
import ovh
import string
import re
import requests
import os
import sys
import logging
import configparser
import socket
from dns import resolver


LOG_FILENAME = 'update.log'
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='[%d/%m/%Y %H:%M:%S %Z]', filename=LOG_FILENAME, level=logging.INFO)
logger = logging.getLogger(__name__)

file_config = 'ovh.conf'
params = {
    "zone_name": "",
    "subdomain": "",
    "id": ""  # Empty and filled later
}

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


def get_external_ip(domain):
    res = resolver.Resolver()
    res.nameservers = ['208.67.222.123', '208.67.220.123',
                       '208.67.222.222', '208.67.220.220', '8.8.8.8', '8.8.4.4']
    answers = res.query(domain)
    response_ip = []
    for rdata in answers:
        response_ip.append(rdata.address)
    return response_ip

def refresh_zone(client, params):
    result = client.post('/domain/zone/' + params['zone_name'] + '/refresh')

def update_ip():
    try:
        config = configparser.ConfigParser(default_section="default")
        with open(file_config) as cf:
            config.read_file(cf)

        client = ovh.Client(config_file='ovh.conf')
        params['zone_name'] = config.get("updater", "zone_name")
        params['subdomain'] = config.get("updater", "subdomain")

        dns_current_ip = socket.gethostbyname(params['subdomain'])

        # TODO replace with custom docker IP checker
        #r = requests.get("http://ip.socketz.net/json")
        r = requests.get("http://ifconfig.co/json")

        if r.status_code == 200:
            result = r.json()
            ip_address = result['ip']

            if dns_current_ip != ip_address:

                if params['id'] == "":
                    result = client.get(
                        '/domain/zone/' + params['zone_name'] + '/dynHost/record', subDomain=params['subdomain'])
		    
                    if len(result) == 0:
			result = client.post('/domain/zone/' + params['zone_name'] + '/dynHost/record', ip=ip_address, subDomain=params['subdomain'])
			refresh_zone(client, params)
                        msg = "Created subdomain {!s} with IP address {!s}".format(params['subdomain'], ip_address)
			logger.info(msg)
			print(msg)
                        sys.exit(1)

                    params['id'] = str(result[0])

                    msg = "Record ID: " + params['id']
                    logger.info(msg)
                    print(msg)

                current_record = client.get(
                    '/domain/zone/' + params['zone_name'] + '/dynHost/record/' + params['id'])

                if current_record['ip'] != ip_address:
		    result_del = client.delete('/domain/zone/' + params['zone_name'] + '/dynHost/record/' + params['id'])
                    result = client.post('/domain/zone/' + params['zone_name'] + '/dynHost/record', ip=ip_address, subDomain=params['subdomain'])

                    if result == None:
			refresh_zone(client, params)
                        msg = "Successfully updated subdomain {0} with ip address {1}".format(
                            params["subdomain"], ip_address)
                        logger.info(msg)
                        print(msg)
                    else:
                        # Pretty print
                        msg = json.dumps(result, indent=4)
                        logger.info(msg)
                        print(msg)
                else:
                    msg = "Successfully updated subdomain {0} with ip address {1}. Waiting for DNS refreshing...".format(
                        params["subdomain"], ip_address)
                    logger.info(msg)
                    print(msg)
            else:
                msg = "Current ip address ({0}) for subdomain {1} are the same. Not updated.".format(
                    ip_address, params["subdomain"])
                logger.info(msg)
                print(msg)
        else:
            msg = "Cannot get the current external ip"
            logger.error(msg, exc_info=True)
            print(msg)

    except Exception as e:
        logger.error(e, exc_info=True)
        print(e)


if __name__ == '__main__':
    update_ip()
    sys.exit(0)
