#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json, ovh, string, re

params = {
	"zone_name": "socketz.net",
	"subdomain": "home-vpn",
	"id": ""
}


# create a client
client = ovh.Client(config_file='ovh.conf')

# /domain/zone/{zoneName}/dynHost/login/{login}

result = json.loads(client.get('/domain/zone/'+params['zone_name']+'/dynHost/record', subDomain=params['subdomain']))
params['id'] = result[0]

result = client.get('/domain/zone/'+params['zone_name']+'/dynHost/record/'+params['id'])

print json.dumps(result, indent=4)

