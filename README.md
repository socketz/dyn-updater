# Dyn-Updater

Dynamic IP Updater using a dynamic DNS provider

Compatible with python 2/3

###### NOTE: At the moment using only OVH API.

## How to use (OVH)

First of all, read documentation from [python-ovh](https://github.com/ovh/python-ovh)

1. Install requirements with `pip install -r requirements.txt`
2. Create a key and secret at [https://eu.api.ovh.com/createApp/](https://eu.api.ovh.com/createApp/) (use your correct endpoint: eu, us, etc)
3. Put the key and secret in ovh.conf
4. Execute *auth.py* for request a consumer key
5. Put your consumer key in ovh.conf
6. Create a cron task for dyn-updater.py and done! (see below)

BONUS: May use config.py file for automated configuration step by step.

### Example of cron task:
```bash
*/10 * * * * /usr/bin/python /root/dyn-updater/dyn-updater.py >> /root/dyn-updater/update.log 2>&1
```
