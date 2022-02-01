#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
import sys
import time
import configparser
import ovh


class ConfUpdater():

    file_config = 'ovh.conf'
    ep = ""  # Endpoint
    app_key = ""  # Application key
    app_secret = ""  # Application secret

    zone_name = ""
    subdomain = ""

    links = {
        1: "https://eu.api.ovh.com/createApp/",
        2: "https://ca.api.ovh.com/createApp/",
        3: "https://eu.api.soyoustart.com/createApp/",
        4: "https://ca.api.soyoustart.com/createApp/",
        5: "https://eu.api.kimsufi.com/createApp/",
        6: "https://ca.api.kimsufi.com/createApp/",
    }

    def __init__(self):
        pass

    def menu(self):
        try:
            print("""
                1. 'ovh-eu' for OVH Europe API
                2. 'ovh-ca' for OVH North-America API
                3. 'soyoustart-eu' for So you Start Europe API
                4. 'soyoustart-ca' for So you Start North America API
                5. 'kimsufi-eu' for Kimsufi Europe API
                6. 'kimsufi-ca' for Kimsufi North America API
            """)

            endp = input('Choose your endpoint [1]: ')

            if endp == '':
                return 1

            endp = int(endp)

            self.ep = {
                1: "ovh-eu",
                2: "ovh-ca",
                3: "soyoustart-eu",
                4: "soyoustart-ca",
                5: "kimsufi-eu",
                6: "kimsufi-ca"
            }[endp]

            print("Selected {} endpoint".format(self.ep))

            input("Please, put your login credentials, and copy application data on this link {} \n"
                  "If you have an existent application, put your application data. \n"
                  "If you do not remember it, access to https://api.ovh.com/ , remove the app, and make another one.\n"
                  "Press Enter key to continue...".format(
                      self.links[endp]))

            # Set application key
            u_key = input("Put your application_key: ")

            if u_key == '':
                return None

            self.app_key = u_key

            # Set application secret
            u_secret = input("Put your application_secret: ")

            if u_secret == '':
                return None

            self.app_secret = u_secret

            return self.ep
        except KeyboardInterrupt:
            print("\n")
            sys.exit(0)

    def menu_client(self):
        try:

            self.zone_name = input('Put your zone_name (example.com): ')
            self.subdomain = input('Put your subdomain (mysubdomain): ')

            print("""
                1. Request Safe RW (GET,PUT,POST) to path /* API access
                2. Request RW (GET,PUT,POST,DELETE) to path /* API access
            """)

            type_request = input('Choose your type requests [1]: ')

            if type_request == '':
                type_request = 1

            return int(type_request)
        except KeyboardInterrupt:
            print("\n")
            sys.exit(0)

    def start(self):
        endp = self.menu()

        if endp != None:
            config = configparser.ConfigParser(
                allow_no_value=True, default_section="default")
            config.set("default", "endpoint", endp)
            config.add_section(endp)
            config.set(endp, "application_key", self.app_key)
            config.set(endp, "application_secret", self.app_secret)

            self.main_url = input(
                "Main URL endpoint to get your external IP: ")
            self.backup_url = input("Backup URL to get your extrenal IP: ")
            config.add_section('external-ip')
            config.set('external-ip', 'main_url', self.main_url)
            config.set('external-ip', 'backup_url', self.backup_url)

            with open(self.file_config, 'w') as cf:
                config.write(cf)
                print("Configuration file was created.")

            client = ovh.Client(config_file=self.file_config)

            ck = client.new_consumer_key_request()

            request_type = self.menu_client()

            if(request_type == 1):
                # Request Safe RW (GET,PUT,POST) to path /* API access
                ck.add_rules(ovh.API_READ_WRITE_SAFE, "/*")
            else:
                # Request RW (GET,PUT,POST,DELETE) to path /* API access
                ck.add_rules(ovh.API_READ_WRITE, "/*")

            try:
                # Request token
                validation = ck.request()
            except Exception as e:
                print("OVH Exception: ", e)
                sys.exit(1)

            input("Please visit %s to authenticate and after validation success, press Enter to continue..." %
                  validation['validationUrl'])

            # Print nice welcome message
            print("Welcome", client.get('/me')['firstname'])
            print("Btw, your 'consumerKey' is '%s'" %
                  validation['consumerKey'])

            print("Writing changes to %s file..." % self.file_config)
            config = configparser.ConfigParser()
            config.read_file(open(self.file_config))
            config.set(endp, "consumer_key", validation['consumerKey'])

            config.add_section("updater")
            config.set("updater", "zone_name", self.zone_name)
            config.set("updater", "subdomain", self.subdomain)

            with open(self.file_config, "w") as cf:
                config.write(cf)

            print("Configuration done!!")
        else:
            print("Configuration file was not created.")


if __name__ == '__main__':
    if (sys.version_info > (3, 0)):
        c = ConfUpdater()
        c.start()
    else:
        # Python 2 not supported
        print("Please upgrade your python version or use virtualenv")
