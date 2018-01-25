#!/bin/bash

CONF_PATH="/etc/dyn-updater"
BIN_PATH="/usr/local/bin"

# sudo mkdir $CONF_PATH/
# sudo cp ./dyn-updater.py $BIN_PATH/dyn-updater
# sudo chmod 700 $BIN_PATH/dyn-updater
# sudo ln -s $CONF_PATH/ovh.conf $BIN_PATH/ovh.conf


echo '
	#!/bin/sh
	#./etc/rc.d/init.d/functions    #descomente/modifique para su killproc
	case "$1" in
	  start)
	    echo "Starting dyn-updater..."
	    {$BIN_PATH}/dyn-updater
	  ;;
	  stop)
	    echo -n "Stopping dyn-updater..."
	    killproc -TERM {$BIN_PATH}/dyn-updater
	  ;;
	  *)
	    echo "Uso: $0 {start|stop}"
	    exit 1
	esac
	exit 0
'


# https://github.com/kylemanna/docker-openvpn.git
