#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import ovh
import string
import re
from tabulate import *


try:
    print("Giving current token status: \n")
    client = ovh.Client(config_file='ovh.conf')

    credentials = client.get('/me/api/credential', status='validated')

    # pretty print credentials status
    table = []
    for credential_id in credentials:
        credential_method = '/me/api/credential/' + str(credential_id)
        credential = client.get(credential_method)
        application = client.get(credential_method + '/application')

        table.append([
            credential_id,
            '[%s] %s' % (application['status'], application['name']),
            application['description'],
            credential['creation'],
            credential['expiration'],
            credential['lastUse'],
        ])
    print(tabulate(table, headers=['ID', 'App Name', 'Description',
                                   'Token Creation', 'Token Expiration', 'Token Last Use']))
    credentialId_opt = input("Do you want to delete a credentialId? [yY/nN]: ").lower()
    if credentialId_opt == 'y':
        credentialId = input("Put the credentialId: ")
        delete_endp = f"/me/api/credential/{credentialId}"
        results = client.delete(delete_endp)
        if(results == None):
            print("ID {!s} deleted".format(credentialId))

except Exception as e:
    print(e)
