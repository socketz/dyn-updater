#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json, ovh, string, re, requests
from tabulate import * 

params = {
	"zone_name": "socketz.net",
	"subdomain": "home-vpn",
	"id": "" # Empty and filled later
}

try:
	client = ovh.Client(config_file='ovh.conf')

	if params['id'] == "":
		result = client.get('/domain/zone/'+params['zone_name']+'/dynHost/record', subDomain=params['subdomain'])
		params['id'] = str(result[0])
		print "Record ID: "+params['id']

	current_record = client.get('/domain/zone/'+params['zone_name']+'/dynHost/record/'+params['id'])

	r = requests.get("http://ifconfig.co/json")

	if r.status_code == 200:
		result = r.json()
		ip_address = result["ip"]
		
		if ip_address != current_record["ip"]:
		
			result = client.put('/domain/zone/'+params['zone_name']+'/dynHost/record/'+params['id'], ip=ip_address, subDomain=params['subdomain'])

			if result == None:
				print "Successfully updated subdomain {0} with ip address {1}".format(params["subdomain"], ip_address)
			else:
				# Pretty print
				print json.dumps(result, indent=4)
		else:
			print "Current ip address ({0}) for subdomain {1} are the same. Not updated.".format(ip_address, params["subdomain"])
	else:
		print "Cannot get the current external ip"

except Exception, e:
	print e