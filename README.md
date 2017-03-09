# Dyn-Updater OVH

## How to use

First of all, read documentation from [python-ovh](https://github.com/ovh/python-ovh)

1. Create a key and secret at [https://eu.api.ovh.com/createApp/](https://eu.api.ovh.com/createApp/) (use your correct endpoint: eu, us, etc)
2. Put the key and secret in ovh.conf
3. Execute auth.py for request a consumer key
4. Put your consumer key in ovh.conf
5. Change parameters of dyn-updater.py and execute it
6. Cron a job for dyn-updater.py and done!