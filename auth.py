#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json
import ovh

client = ovh.Client()

# Request RO, /me API access
ck = client.new_consumer_key_request()
ck.add_rules(ovh.API_READ_WRITE, "/*")

# Request token
validation = ck.request()

print "Please visit %s to authenticate" % validation['validationUrl']
raw_input("and press Enter to continue...")

# Print nice welcome message
print "Welcome", client.get('/me')['firstname']
print "Btw, your 'consumerKey' is '%s'" % validation['consumerKey']