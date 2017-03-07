#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json, ovh, string, re
from tabulate import * 

params = {
	"zone_name": "socketz.net",
	"subdomain": "home-vpn",
	"id": ""
}

try:
	# Instanciate an OVH Client.
	# You can generate new credentials with full access to your account on
	# the token creation page
	client = ovh.Client(config_file='ovh.conf')

	# result = client.get('/auth/currentCredential')
	# result = json.loads(client.get('/domain/zone/'+params['zone_name']+'/dynHost/record', subDomain=params['subdomain']))
	result = client.get('/domain/zone/'+params['zone_name']+'/dynHost/record', subDomain=params['subdomain'])
	params['id'] = str(result[0])

	result = client.get('/domain/zone/'+params['zone_name']+'/dynHost/record/'+params['id'])

	# Pretty print
	print json.dumps(result, indent=4)

	# curl ifconfig.co
	# /domain/zone/{zoneName}/dynHost/record/{id}
	# update
	# result = client.put('/domain/zone/'+params['zone_name']+'/dynHost/record/'+params['id'], ip=)

except Exception, e:
	print e

# create a client
# client = ovh.Client(config_file='ovh.conf')

# /domain/zone/{zoneName}/dynHost/login/{login}

# result = json.loads(client.get('/domain/zone/'+params['zone_name']+'/dynHost/record', subDomain=params['subdomain']))
# params['id'] = result[0]

# result = client.get('/domain/zone/'+params['zone_name']+'/dynHost/record/'+params['id'])

# print json.dumps(result, indent=4)

