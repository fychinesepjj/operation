#!/bin/bash
#
# This scripts is used to stop the application.
#
#
#

sudo service nginx stop
# remove nginx  cache
sudo rm -fr /var/lib/nginx/cache
