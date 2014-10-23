#!/bin/bash
#
# This scripts is used to install the application.
# This scripts is required for all projects.
#
#
#
SCRIPT_DIR=`dirname $0`

if [ "$1" = "checkdeps" ] ; then
	echo "Checking and installing dependecies..."
    if [ -f "${SCRIPT_DIR}/install_deps.sh" ]; then
        ${SCRIPT_DIR}/install_deps.sh
	else
		echo "Depedency install script not found."
    fi
fi

PROJECT=seabedop
USER=seabedop

echo "Collect Static to  Webfront "

#python manage.py collectstatic

echo Configuring ${PROJECT}...

#echo Installing operation...
#[ -z `grep "^$USER:" /etc/passwd` ] && sudo useradd -r $USER -M -N

#chmod -R a+rw /var/app/data/$PROJECT
#chmod -R a+rw /var/app/log/$PROJECT
#chown $USER:nogroup /var/app/data/$PROJECT
#chown $USER:nogroup /var/app/log/$PROJECT

#ln -sf /var/app/enabled/$PROJECT/scripts/seabed-operation-init.sh /etc/init.d/seabed-operation
#update-rc.d seabed-operation defaults

#cp /var/app/enabled/$PROJECT/scripts/seabedop.cron /etc/cron.d/seabedop
