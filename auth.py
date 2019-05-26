#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import ovh
import configparser


filename = "ovh.conf"

client = ovh.Client(config_file=filename)

ck = client.new_consumer_key_request()

# Request Safe RW (GET,PUT,POST) to path /* API access
ck.add_rules(ovh.API_READ_WRITE_SAFE, "/*")

# Request RW (GET,PUT,POST,DELETE) to path /* API access
# ck.add_rules(ovh.API_READ_WRITE, "/*")

# Request token
validation = ck.request()

print("Please visit %s to authenticate" % validation['validationUrl'])
input("and after validation success, press Enter to continue...")

# Print nice welcome message
print("Welcome", client.get('/me')['firstname'])
print("Btw, your 'consumerKey' is '%s'" % validation['consumerKey'])

print("Writing changes to %s file..." % filename)
config = configparser.ConfigParser()
config.read_file(open(filename))

endp = config.get("endpoint")
config.set(endp, validation['consumerKey'])

with open(filename, "w") as cf:
    config.write(cf)

print("Done!!")
