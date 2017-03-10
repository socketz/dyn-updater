#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json, ovh, string, re, requests, os
from tabulate import * 
import logging

LOG_FILENAME = 'update.log'
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='[%d/%m/%Y %H:%M:%S %Z]', filename=LOG_FILENAME, level=logging.INFO)

params = {
	"zone_name": "socketz.net",
	"subdomain": "home-vpn",
	"id": "" # Empty and filled later
}

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

try:
	client = ovh.Client(config_file='ovh.conf')

	if params['id'] == "":
		result = client.get('/domain/zone/'+params['zone_name']+'/dynHost/record', subDomain=params['subdomain'])
		params['id'] = str(result[0])
		
		msg = "Record ID: "+params['id']
		logging.info(msg)
		print msg

	current_record = client.get('/domain/zone/'+params['zone_name']+'/dynHost/record/'+params['id'])

	r = requests.get("http://ifconfig.co/json")

	if r.status_code == 200:
		result = r.json()
		ip_address = result["ip"]
		
		if ip_address != current_record["ip"]:
		
			result = client.put('/domain/zone/'+params['zone_name']+'/dynHost/record/'+params['id'], ip=ip_address, subDomain=params['subdomain'])

			if result == None:
				msg = "Successfully updated subdomain {0} with ip address {1}".format(params["subdomain"], ip_address)
				logging.info(msg)
				print msg
			else:
				# Pretty print
				msg = json.dumps(result, indent=4)
				logging.info(msg)
				print msg
		else:
			msg = "Current ip address ({0}) for subdomain {1} are the same. Not updated.".format(ip_address, params["subdomain"])
			logging.info(msg)
			print msg
	else:
		msg = "Cannot get the current external ip"
		logging.error(msg)
		print msg

except Exception, e:
	logging.error(e)
	print e