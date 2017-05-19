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

LOG_FILENAME = 'update.log'
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='[%d/%m/%Y %H:%M:%S %Z]', filename=LOG_FILENAME, level=logging.INFO)

file_config = 'ovh.conf'
params = {
    "zone_name": "",
    "subdomain": "",
    "id": ""  # Empty and filled later
}

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


def update_ip():
    try:
        config = configparser.ConfigParser(default_section="default")
        with open(file_config) as cf:
            config.read_file(cf)

        client = ovh.Client(config_file='ovh.conf')
        params['zone_name'] = config.get("updater", "zone_name")
        params['subdomain'] = config.get("updater", "subdomain")

        ovh_current_ip = socket.gethostbyname(params['subdomain'])

        # TODO replace with custom docker IP checker
        r = requests.get("http://ifconfig.co/json")

        if r.status_code == 200:
            result = r.json()
            ip_address = result["ip"]

            if ovh_current_ip != ip_address:

                if params['id'] == "":
                    result = client.get(
                        '/domain/zone/' + params['zone_name'] + '/dynHost/record', subDomain=params['subdomain'])

                    if len(result) == 0:
                        print("Please, check your DNS configuration... Exiting.")
                        sys.exit(1)

                    params['id'] = str(result[0])

                    msg = "Record ID: " + params['id']
                    logging.info(msg)
                    print(msg)

                current_record = client.get(
                    '/domain/zone/' + params['zone_name'] + '/dynHost/record/' + params['id'])
                result = client.put('/domain/zone/' + params['zone_name'] + '/dynHost/record/' + params[
                    'id'], ip=ip_address, subDomain=params['subdomain'])

                if result == None:
                    msg = "Successfully updated subdomain {0} with ip address {1}".format(
                        params["subdomain"], ip_address)
                    logging.info(msg)
                    print(msg)
                else:
                    # Pretty print
                    msg = json.dumps(result, indent=4)
                    logging.info(msg)
                    print(msg)
            else:
                msg = "Current ip address ({0}) for subdomain {1} are the same. Not updated.".format(
                    ip_address, params["subdomain"])
                logging.info(msg)
                print(msg)
        else:
            msg = "Cannot get the current external ip"
            logging.error(msg)
            print(msg)

    except Exception as e:
        logging.error(e)
        print(e)


if __name__ == '__main__':
    if (sys.version_info > (3, 0)):
        update_ip()
        sys.exit(0)
    else:
        # Python 2 not supported
        print("Please upgrade your python version or use virtualenv")
        sys.exit(1)
